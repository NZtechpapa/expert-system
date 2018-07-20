# -*- coding:utf-8 -*-
# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json
import logging
from datetime import date
from horizon import exceptions
from horizon import tables
from horizon import version
from horizon import messages
from horizon import workflows
from horizon import forms

from django import shortcuts
from django import http
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy

from openstack_dashboard.dashboards.admin.expertmgmt import tables as project_tables
from openstack_dashboard.dashboards.admin.expertmgmt import workflows as project_workflows
from openstack_dashboard.dashboards.admin.expertmgmt import forms as project_forms

from openstack_dashboard.utils import expert_db_handle

LOG = logging.getLogger(__name__)

def check_expert_state(expected_states):
    def wrapper1(func):
        def wrapper2(self, *args, **kwargs):
            expertid = self.kwargs.get('expertid', None)
            if not expertid:
                raise exceptions.NotAuthorized("Missing Expert ID")
            expert = expert_db_handle.GetExpertInstanceById(expertid)
            if not expert:
                raise exceptions.NotAuthorized("Invalid Expert ID")
            if not expert.state in expected_states:
                raise exceptions.NotAuthorized("Illegal Expert state")
            return func(self, *args, **kwargs)
        return wrapper2
    return wrapper1

def get_experts_data(user_data, filters=[], excluders=[]):
    filters1 = []
    filters2 = []
    operator = ""
    if user_data:
        (filters1, filters2, operator) = expert_db_handle.generate_filter(user_data)
    if filters:
        filters1.extend(filters)
    # Search experts
    return expert_db_handle.QueryExperts(
               filters1, filters2=filters2, operator=operator,
               excluders=excluders)

class IndexView(tables.DataTableView):
    table_class = project_tables.ExpertsTable
    template_name = 'admin/expertmgmt/index.html'
    page_title = u"专家列表"

    def get_data(self):
        user_data = expert_db_handle.get_initial_user_data(self.request.GET, default=False)
        filters = []
        _filters = {}
        excluders = []
        operator = ''
        if self.request.POST:
            _filters = self.get_filters()

        if not _filters:
            if not user_data:
                excluders = [{'var': 'state', 'operator': 'exact', 'words': 'deleted'}]
        elif type(_filters) is dict:
            expert_db_handle.dict2filter(filters, _filters)
        result = get_experts_data(user_data, filters=filters, excluders=excluders)
        return sorted(result, key=lambda d : d.updated_at, reverse=True)

def extract_fields_from_list(context, src_list, format_fields, id_field, max_slices):
    id_range = range(1, 1 + max_slices)
    for s in src_list:
        _id = s[id_field]
        if _id in id_range:
            for fname in format_fields:
                context["%s%s" % (fname, _id)] = s[fname]

def FillContextByexpertid(context, expertid):
    expert_dict = expert_db_handle.GetExpertInstanceById(expertid, returnDict=True)
    if not expert_dict:
        messages.error(self.request, u"无法查询到该ID(%s)的专家记录" % expertid)
        return
    for key in expert_dict:
        context[key] = expert_dict[key]

    rst = expert_db_handle.GetAllExpertTitle(expertid)
    context["rencaichenghaos"] = rst
    rst = expert_db_handle.GetAllExpertClass(expertid)
    context["zhuanjialeixings"] = rst

    rst = expert_db_handle.GetAllExpertDomain(expertid, returnDict=True)
    extract_fields_from_list(
        context, rst,
        project_workflows._EXPERTDOMAINFIELDS,
        'domainserial',
        project_workflows.MAX_EXPERTDOMAIN_SLICES)

    rst = expert_db_handle.GetAllFormalJob(expertid, returnDict=True)
    extract_fields_from_list(
        context, rst,
        project_workflows._EXPERTFORMALJOBFIELDS,
        'formaljob_serial',
        project_workflows.MAX_EXPERTFORMALJOB_SLICES)

    rst = expert_db_handle.GetAllEducation(expertid, returnDict=True)
    extract_fields_from_list(
        context, rst,
        project_workflows._EXPERTEDUCATIONFIELDS,
        'education_serial',
        project_workflows.MAX_EXPERTEDUCATION_SLICES)

    rst = expert_db_handle.GetAllPartTimeJob(expertid, returnDict=True)
    extract_fields_from_list(
        context, rst,
        project_workflows._EXPERTPARTTIMEJOBFIELDS,
        'parttimejob_serial',
        project_workflows.MAX_EXPERTPARTTIMEJOB_SLICES)

    rst = expert_db_handle.GetAllReviewHistory(expertid, returnDict=True)
    extract_fields_from_list(
        context, rst,
        project_workflows._EXPERTREVIEWHISTORYFIELDS,
        'reviewhistory_serial',
        project_workflows.MAX_EXPERTREVIEWHISTORY_SLICES)

    rst = expert_db_handle.GetAllXiangmuInfo(expertid, returnDict=True)
    extract_fields_from_list(
        context, rst,
        project_workflows._EXPERTXIANGMUINFOFIELDS,
        'xiangmuinfo_serial',
        project_workflows.MAX_EXPERTXIANGMUINFO_SLICES)

    rst = expert_db_handle.GetAllAttachment(expertid, returnDict=True)
    extract_fields_from_list(
        context, rst,
        project_workflows._EXPERTATTACHMENTFIELDS,
        'attachment_serial',
        project_workflows.MAX_EXPERTATTACHMENT_SLICES)

class UpdateView(workflows.WorkflowView):
    template_name = 'admin/expertmgmt/update.html'
    workflow_class = project_workflows.UpdateExpertRecord
    page_title = u"修改专家信息"
    policy_rules = (("expertreview", "expertreview:view:updateexpert"),)

    @check_expert_state(['draft'])
    def get_initial(self):
        initial = super(UpdateView, self).get_initial()
        expertid = self.kwargs['expertid']
        FillContextByexpertid(initial, expertid)
        return initial

class DetailView(workflows.WorkflowView):
    template_name = 'admin/expertmgmt/detail.html'
    workflow_class = project_workflows.DetailExpertRecord
    page_title = u"专家信息"
    policy_rules = (("expertreview", "expertreview:view:viewexpert"),)

    def get_initial(self):
        initial = super(DetailView, self).get_initial()
        expertid = self.kwargs['expertid']
        FillContextByexpertid(initial, expertid)
        return initial

class CreateView(workflows.WorkflowView):
    template_name = 'admin/expertmgmt/create.html'
    workflow_class = project_workflows.CreateExpertRecord
    page_title = u"录入专家信息"
    policy_rules = (("expertreview", "expertreview:view:createexpert"),)

class SearchView(forms.ModalFormView):
    template_name = 'admin/expertmgmt/search.html'
    form_id = "searchexpert"
    form_class = project_forms.SearchForm
    submit_label = u"搜索"
    cancel_label = u"取消"
    modal_header = u"高级搜索"
    submit_url = reverse_lazy('horizon:admin:expertmgmt:search')
    url = "horizon:admin:expertmgmt:index"
    page_title = u"输入搜索条件"
    policy_rules = (("expertreview", "expertreview:view:searchexpert"),)

    # As it's ajax form, shall not change the original url
    def get_success_url(self):
        return ''

    def form_valid(self, form):
        try:
            handled = form.handle(self.request, form.cleaned_data)
        except Exception:
            handled = None
            exceptions.handle(self.request)
        if handled and isinstance(handled, http.QueryDict):
            success_url = self.get_success_url()
            url = '%s?%s' % (success_url, handled.urlencode())
            return http.HttpResponseRedirect(url)
        else:
            return self.form_invalid(form)
        

    def get_context_data(self, *args, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['SEARCHPARAM'] = json.dumps(expert_db_handle.SEARCHPARAM)
        context['cancel_url'] = reverse(self.url)
        return context

    def get_initial(self):
        initial = expert_db_handle.get_initial_user_data(self.request.GET, default=True)
        return initial

