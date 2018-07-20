# -*- coding:utf-8 -*-

import logging
from horizon import exceptions
from horizon import tables
from horizon import version
from horizon import messages
from horizon import workflows
from horizon import forms

from django import shortcuts
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from openstack_dashboard.dashboards.project.review import tables as project_tables
from openstack_dashboard.dashboards.project.review import forms as project_forms

from openstack_dashboard.utils import expert_db_handle
from openstack_dashboard.utils import project_db_handle

LOG = logging.getLogger(__name__)

class FillReviewContentView(forms.ModalFormView):
    template_name = 'project/review/review.html'
    form_id = "fill_review_content"
    form_class = project_forms.FillReviewContentForm
    submit_label = u"提交评审报告"
    cancel_label = u"放弃"
    _modal_header = u"评审项目《%s》"
    _submit_url = 'horizon:project:review:doreview'
    success_url = reverse_lazy('horizon:project:review:index')
    url = 'horizon:project:review:index'
    page_title = u"填写项目评审报告"
    policy_rules = (("expertreview", "expertreview:view:fill_review_content"),)

    def get_success_url(self):
        return self.success_url

    def get_context_data(self, *args, **kwargs):
        _args = (self.kwargs['projectid'],)
        self.submit_url = reverse(self._submit_url, args=_args)
        context = super(FillReviewContentView, self).get_context_data(*args, **kwargs)
        return context

    def get_initial(self):
        redirect = reverse("horizon:settings:user:index")
        initial = super(FillReviewContentView, self).get_initial()
        projectid = self.kwargs['projectid']
        expertid = expert_db_handle.get_expertid_from_keystone_user(
            self.request, redirect=redirect)
        try:
            project = project_db_handle.GetProjectInstanceById(projectid)
            reviewer = project_db_handle.GetReviewerInstanceById(project, expertid,
                project_expected_states=['start_review', 'finished'])
        except Exception as e:
            exceptions.handle(self.request,
                              e.message,
                              redirect=redirect)

        initial['projectid'] = projectid
        initial['id'] = reviewer.id
        initial['comments'] = reviewer.comments
        initial['comments_attachments'] = reviewer.comments_attachments
        if project.projectname:
            self.modal_header = self._modal_header % project.projectname
        else:
            self.modal_header = self._modal_header % u'-'
        return initial

class ViewReviewContentView(FillReviewContentView):
    template_name = 'project/review/review.html'
    form_id = 'view_review_content'
    form_class = project_forms.ViewReviewContentForm
    cancel_label = u"放弃"
    #cancel_url = reverse_lazy('horizon:project:review:index')
    _modal_header = u"项目《%s》评审内容"
    success_url = reverse_lazy('horizon:project:review:index')
    submit_label = None
    submit_url = None
    url = reverse_lazy('horizon:project:review:index')
    page_title = u"查看项目评审内容"
    policy_rules = (("expertreview", "expertreview:view:view_review_content"),)


    def get_context_data(self, *args, **kwargs):
        self.submit_url = ""
        context = super(ViewReviewContentView, self).get_context_data(*args, **kwargs)
        return context

class IndexView(tables.DataTableView):
    table_class = project_tables.ReviewTable
    template_name = 'project/review/index.html'
    page_title = u"项目列表"

    def get_data(self):
        redirect = reverse("horizon:settings:user:index")
        expertid = expert_db_handle.get_expertid_from_keystone_user(
            self.request, redirect=redirect)
        return project_db_handle.GetReviewerProjects(expertid)

