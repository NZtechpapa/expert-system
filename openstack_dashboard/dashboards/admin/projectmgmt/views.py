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
from datetime import datetime
from horizon import exceptions
from horizon import tables
from horizon import version
from horizon import messages
from horizon import workflows
from horizon import forms

from django import shortcuts
from django import http
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy

from openstack_dashboard.dashboards.admin.projectmgmt import tables as project_tables
from openstack_dashboard.dashboards.admin.projectmgmt import workflows as project_workflows
from openstack_dashboard.dashboards.admin.projectmgmt import forms as project_forms

from openstack_dashboard.dashboards.admin.expertmgmt import views as expertmgmt_views

from openstack_dashboard.models import REVIEWER_SELECTED
from openstack_dashboard.utils import expert_db_handle
from openstack_dashboard.utils import project_db_handle

LOG = logging.getLogger(__name__)
# 专家信息保存文档
import sys
from docx import Document
from docx.shared import Inches

def check_project_state(expected_states):
    def wrapper1(func):
        def wrapper2(self, *args, **kwargs):
            projectid = self.kwargs.get('projectid', None)
            if not projectid:
                raise exceptions.NotAuthorized("Missing Project ID")
            project = project_db_handle.GetProjectInstanceById(projectid)
            if not project:
                raise exceptions.NotAuthorized("Invalid Project ID")
            if not project.state in expected_states:
                raise exceptions.NotAuthorized("Illegal Project state")
            return func(self, *args, **kwargs)
        return wrapper2
    return wrapper1

def FillContextByprojectid(context, projectid):
    project_dict = project_db_handle.GetProjectInstanceById(projectid, returnDict=True)
    if not project_dict:
        messages.error(self.request, u"无法查询到该ID(%s)的项目记录" % projectid)
        return
    for key in project_dict:
        if type(project_dict[key]) == date:
            context[key] = project_dict[key].strftime("%Y-%m-%d")
        elif type(project_dict[key]) == datetime:
            context[key] = project_dict[key].isoformat()
        else:
            context[key] = project_dict[key]

class IndexView(tables.DataTableView):
    table_class = project_tables.ProjectsTable
    template_name = 'admin/projectmgmt/index.html'
    page_title = u"项目列表"

    def get_data(self):
        user_data = project_db_handle.get_initial_user_data(self.request.GET, default=False)
        if self.request.POST:
            _filters = self.get_filters()
        else:
            _filters = {}
        filters = []
        filters1 = []
        filters2 = []
        operator = ''
        if type(_filters) is dict:
            project_db_handle.dict2filter(filters, _filters)
        if not user_data and not filters:
            return sorted(project_db_handle.GetProjects(),
                          key=lambda d : d.updated_at,
                          reverse=True)
        if user_data:
            (filters1, filters2, operator) = project_db_handle.generate_filter(user_data)
        if filters:
            filters1.extend(filters)
        return project_db_handle.QueryProjects(filters1, filters2, operator)

class SearchProjectView(expertmgmt_views.SearchView):
    template_name = 'admin/projectmgmt/searchproject.html'
    form_id = 'searchproject'
    form_class = project_forms.SearchForm
    submit_label = u"搜索"
    cancel_label = u"取消"
    modal_header = u"高级搜索"
    submit_url = reverse_lazy('horizon:admin:projectmgmt:searchproject')
    success_url = reverse_lazy('horizon:admin:projectmgmt:index')
    url = "horizon:admin:projectmgmt:index"
    page_title = u"输入搜索条件"
    policy_rules = (("expertreview", "expertreview:view:searchproject"),)

    def get_context_data(self, *args, **kwargs):
        context = super(SearchProjectView, self).get_context_data(**kwargs)
        context['SEARCHPARAM'] = json.dumps(project_db_handle.SEARCHPARAM)
        context['cancel_url'] = reverse(self.url)
        return context

    def get_initial(self):
        initial = project_db_handle.get_initial_user_data(self.request.GET, default=True)
        initial['success_url'] = self.get_success_url()
        return initial

class CreateProjectView(workflows.WorkflowView):
    workflow_class = project_workflows.CreateProjectRecord
    template_name = 'admin/projectmgmt/createproject.html'
    page_title = u"录入项目信息"
    policy_rules = (("expertreview", "expertreview:view:createproject"),)

class UpdateProjectView(workflows.WorkflowView):
    template_name = 'admin/projectmgmt/updateproject.html'
    workflow_class = project_workflows.UpdateProjectRecord
    page_title = u"修改项目信息"
    policy_rules = (("expertreview", "expertreview:view:updateproject"),)

    @check_project_state(['draft'])
    def get_initial(self):
        initial = super(UpdateProjectView, self).get_initial()
        projectid = self.kwargs['projectid']
        FillContextByprojectid(initial, projectid)
        return initial

class ViewProjectView(workflows.WorkflowView):
    template_name = 'admin/projectmgmt/viewproject.html'
    workflow_class = project_workflows.DetailProjectRecord
    page_title = u"项目信息"
    policy_rules = (("expertreview", "expertreview:view:viewproject"),)

    def get_initial(self):
        initial = super(ViewProjectView, self).get_initial()
        projectid = self.kwargs['projectid']
        FillContextByprojectid(initial, projectid)
        return initial

class SetRuleView(forms.ModalFormView):
    template_name = 'admin/projectmgmt/setrule.html'
    form_id = 'setrule'
    page_title = u"设置抽取规则"
    policy_rules = (("expertreview", "expertreview:view:setrule"),)
    form_class = project_forms.SetRuleForm
    submit_label = u"设置"
    cancel_label = u"取消"
    modal_header = u"设置抽取规则"
    _submit_url = 'horizon:admin:projectmgmt:setrule'
    success_url = reverse_lazy('horizon:admin:projectmgmt:index')
    page_title = u"输入抽取条件"

    @check_project_state(['waitfor_setrule'])
    def get_context_data(self, *args, **kwargs):
        projectid = self.kwargs['projectid']
        self.submit_url = reverse(self._submit_url, args=(projectid,))
        context = super(SetRuleView, self).get_context_data(**kwargs)
        project = project_db_handle.GetProjectInstanceById(projectid)
        if project.chouquyaoqiu:
            context['chouquyaoqiu'] = project.chouquyaoqiu
        else:
            context['chouquyaoqiu'] = u"无"
        return context

    def get_initial(self):
        initial = expert_db_handle.get_initial_user_data(self.request.GET, default=True)
        projectid = self.kwargs['projectid']
        project = project_db_handle.GetProjectInstanceById(projectid)
        experts = project_db_handle.GetBindedReviewers(project, need_reviewer_info=False)
        initial['id'] = projectid
        chouqurenshu = (project.chouqurenshu - len(experts))
        if chouqurenshu < 1:
            chouqurenshu = 1
        initial['chouqurenshu'] = chouqurenshu
        return initial

class SearchCandidate2View(expertmgmt_views.SearchView):
    form_id = 'searchcandidate2'
    policy_rules = (("expertreview", "expertreview:view:searchcandidate2"),)

    @check_project_state(['waitfor_setrule', 'waitfor_bind', 'binded'])
    def get_context_data(self, *args, **kwargs):
        context = super(SearchCandidate2View, self).get_context_data(**kwargs)
        projectid = self.kwargs['projectid']
        project = project_db_handle.GetProjectInstanceById(projectid)
        context['chouquyaoqiu'] = project.chouquyaoqiu
        return context

class ManageExpertMin(object):
    def get_project(self):
        projectid = self.kwargs['projectid']
        return project_db_handle.GetProjectInstanceById(projectid)

    def set_page_title(self, project):
        if not getattr(self, '_page_title'):
            return
        self.page_title = self._page_title % project.projectname

class ManageCandidateBase(ManageExpertMin):
    def get_candidates(self, settitle=True):
        project = self.get_project()
        experts = project_db_handle.GetAvailableCandidate(project, need_reviewer_info=True)
        if settitle:
            self.set_page_title(project)
        return experts

class ManageReviewerBase(ManageExpertMin):
    def get_reviewers(self, settitle=True):
        project = self.get_project()
        experts = project_db_handle.GetBindedReviewers(project, need_reviewer_info=True)
        if settitle:
            self.set_page_title(project)
        #if not project.state in ['start_review', 'finished']:
        #    return experts
        #for expert in experts:
        #    expert.review_state = \
        #        project_db_handle.GetReviewerReviewState(project, expert.id)
        return experts

class ManageCandidateView(tables.DataTableView, ManageCandidateBase):
    table_class = project_tables.CandidateTable
    template_name = 'admin/projectmgmt/managecandidate.html'
    _page_title = u"项目《%s》：候选专家列表"

    @check_project_state(['waitfor_bind'])
    def get_data(self):
        return self.get_candidates(settitle=True)

class ManageCandidate2View(tables.MultiTableView, ManageCandidateBase):
    template_name = 'admin/projectmgmt/managecandidate2.html'
    table_classes = (project_tables.MatchCandidate2Table,
                     project_tables.CandidateTable,)
    _page_title = u"项目《%s》：候选专家列表"

    def get_matchcandidate2_data(self):
        user_data = expert_db_handle.get_initial_user_data(self.request.GET, default=False)
        if not user_data:
            return []
        projectid = self.kwargs['projectid']
        project = project_db_handle.GetProjectInstanceById(projectid)
        excluders = [{'var': 'suozaidaiwei', 'operator': 'exact', 'words': project.shenbaodanwei}]
        filters = []
        _filters = {'state': 'approved'}
        expert_db_handle.dict2filter(filters, _filters)
        return expertmgmt_views.get_experts_data(user_data, filters=filters, excluders=excluders)

    @check_project_state(['waitfor_bind', 'binded'])
    def get_candidatetable_data(self):
        return self.get_candidates(settitle=True)

# 管理评审专家列表2（超管专用）
class ManageReviewer2View(tables.MultiTableView, ManageReviewerBase, ManageCandidateBase):
    template_name = 'admin/projectmgmt/managereviewer2.html'
    table_classes = (project_tables.CandidateTable,
                     project_tables.ReviewerTable,
                     project_tables.UnavailableReviewerTable,)
    _page_title = u"项目《%s》：评审专家管理"

    @check_project_state(['waitfor_setrule', 'waitfor_bind', 'binded'])
    def get_candidatetable_data(self):
        return self.get_candidates(settitle=False)

    def get_reviewertable_data(self):
        return self.get_reviewers(settitle=True)

    def get_unavailablereviewertable_data(self):
        projectid = self.kwargs['projectid']
        return project_db_handle.GetUnavailableReviewer(projectid)

# 管理评审专家列表
class ManageReviewerView(tables.DataTableView, ManageReviewerBase):
    template_name = 'admin/projectmgmt/managereviewer.html'
    table_class = project_tables.ReviewerTable
    _page_title = u"项目《%s》：管理评审专家"

    @check_project_state(['waitfor_bind', 'binded'])
    def get_data(self):
        return self.get_reviewers(settitle=True)

def get_age1(expert):
    today = date.today()
    born = expert.born
    try: 
        if born:
            birthday = born.replace(year=today.year)
        else:
            return '-'
    except ValueError: # raised when birth date is February 29 and the current year is not a leap year
        birthday = born.replace(year=today.year, day=born.day-1)
    if birthday > today:
        return "%d" % (today.year - born.year - 1)
    else:
        return "%d" % (today.year - born.year)

#  保存审查专家列表到docx
def write_docx(experts,project):
    today = date.today()
    #fp = open("log.txt","r+")
    #project.name
    #loop = 0;
    #name = ''
    #mail = ''
    #zhicheng = ''
    #suozaidaiwei = ''
    #age = ''
    #for expert in experts:
    #    loop = loop + 1
    #    name = name + expert.expertname
    #    mail = mail + str(expert.email)
    #    zhicheng = zhicheng + str(expert.zhicheng)
    #    suozaidaiwei = suozaidaiwei + str(expert.suozaidaiwei)
    #    age = age + ': ' +str(get_age1(expert))

    #fp.write(str(loop)+ name + 'mail:\n'+ mail +'\n zhicheng:' + zhicheng +'\nchusheng'+ suozaidaiwei + '\nage'+ age)
    #fp.close()
    reload(sys)
    sys.setdefaultencoding('utf-8')
    document = Document('/var/www/expertreview/download/template.docx')

    table = document.tables[0]
    rowindex = 0
   
    for expert in experts:
        rowindex =  rowindex + 1
        row_cells = table.add_row().cells
        row_cells[0].text = str(rowindex).decode('UTF-8')
        row_cells[1].text = str(expert.expertname).decode('UTF-8')
        row_cells[2].text = str(expert.suozaidaiwei).decode('UTF-8')
        row_cells[3].text = str(expert.zhicheng).decode('UTF-8')


    row_cells = table.add_row().cells
    row_cells[0].merge(row_cells[5])
    row_cells[0].text =  u'                               合计： '

    document.save('/var/www/expertreview/download/experts.docx')


       
# 查看评审专家列表
class ViewReviewerView(tables.DataTableView, ManageReviewerBase):
    template_name = 'admin/projectmgmt/viewreviewer.html'
    table_class = project_tables.ReviewerTable
    _page_title = u"项目《%s》：评审专家列表"

    @check_project_state(['kickoff', 'start_review', 'finished'])
    def get_data(self):
        experts = self.get_reviewers(settitle=True)
        project = self.get_project()
        write_docx(experts,project)
        return experts

class StartReviewView(forms.ModalFormView):
    template_name = 'admin/projectmgmt/startreview.html'
    form_id = 'start_review_form'
    form_class = project_forms.StartReviewForm
    submit_label = u"开始项目评审"
    cancel_label = u"取消"
    modal_header = u"开始项目评审"
    _submit_url = 'horizon:admin:projectmgmt:startreview'
    success_url = reverse_lazy('horizon:admin:projectmgmt:index')
    url = "horizon:admin:projectmgmt:index"
    page_title = u"填写文字说明，开始项目评审"
    policy_rules = (("expertreview", "expertreview:view:start_review_form"),)

    def get_success_url(self):
        return self.success_url

    def get_context_data(self, *args, **kwargs):
        _args = (self.kwargs['projectid'], )
        self.submit_url = reverse(self._submit_url, args=_args)
        context = super(StartReviewView, self).get_context_data(*args, **kwargs)
        return context

    @check_project_state(['kickoff'])
    def get_initial(self):
        initial = super(StartReviewView, self).get_initial()
        projectid = self.kwargs['projectid']
        FillContextByprojectid(initial, projectid)
        return initial

# Return a table of all reviewers in this project
class ManageReviewResultView(tables.DataTableView, ManageReviewerBase):
    table_class = project_tables.ManageReviewResultTable
    template_name = 'admin/projectmgmt/managereviewresult.html'
    _page_title = u"项目《%s》：评审管理"

    @check_project_state(['start_review', 'finished'])
    def get_data(self):
        return self.get_reviewers(settitle=True)

# 随机抽取专家，总的项目列表，点击随机抽取
# 1，填写人数
# 2，填写理由
class RandomBindView(forms.ModalFormView):
    template_name = 'admin/projectmgmt/randombind.html'
    form_id = 'random_bind_form'
    form_class = project_forms.RandomBindForm
    submit_label = u"开始抽取"
    cancel_label = u"取消"
    _modal_header = u"项目《%s》：随机抽取评审专家"
    _submit_url = 'horizon:admin:projectmgmt:randombind'
    success_url = 'horizon:admin:projectmgmt:index'
    url = "horizon:admin:projectmgmt:index"
    page_title = u"随机抽取指定数量专家参与项目评审"
    policy_rules = (("expertreview", "expertreview:view:random_bind_form"),)

    def get_success_url(self):
        return reverse(self.success_url)

    def get_context_data(self, *args, **kwargs):
        _args = (self.kwargs['projectid'], )
        self.submit_url = reverse(self._submit_url, args=_args)
        context = super(RandomBindView, self).get_context_data(*args, **kwargs)
        return context

    @check_project_state(['waitfor_bind'])
    def get_initial(self):
        initial = super(RandomBindView, self).get_initial()
        projectid = self.kwargs['projectid']
        project = project_db_handle.GetProjectInstanceById(projectid)
        experts = project_db_handle.GetBindedReviewers(project, need_reviewer_info=False)
        initial['id'] = project.id
        initial['projectname'] = project.projectname
        self.modal_header = self._modal_header % project.projectname
        chouqurenshu = (project.chouqurenshu - len(experts))
        if chouqurenshu < 1:
            chouqurenshu = 1
        initial['chouqurenshu'] = chouqurenshu
        return initial

# Comment single expert's review comments
class CommentExpertReviewView(forms.ModalFormView):
    template_name = 'admin/projectmgmt/addcomment.html'
    form_id = 'comment_expert_review'
    form_class = project_forms.CommentExpertReviewForm
    submit_label = u"提交评论"
    cancel_label = u"放弃"
    modal_header = u"评论该专家提交的评审意见"
    _submit_url = 'horizon:admin:projectmgmt:commentreviewresult'
    success_url = 'horizon:admin:projectmgmt:managereviewresult'
    url = "horizon:admin:projectmgmt:index"
    page_title = u"评论该专家提交的评审意见"
    policy_rules = (("expertreview", "expertreview:view:comment_expert_review"),)

    def get_success_url(self):
        return reverse(self.success_url,
                       args=(self.kwargs['projectid'],))

    def get_context_data(self, *args, **kwargs):
        _args = (self.kwargs['projectid'], self.kwargs['expertid'],)
        self.submit_url = reverse(self._submit_url, args=_args)
        context = super(CommentExpertReviewView, self).get_context_data(*args, **kwargs)
        return context

    @check_project_state(['finished'])
    def get_initial(self):
        initial = super(CommentExpertReviewView, self).get_initial()
        projectid = self.kwargs['projectid']
        expertid = self.kwargs['expertid']
        project = project_db_handle.GetProjectInstanceById(projectid)
        expert = expert_db_handle.GetExpertInstanceById(expertid)
        initial['projectid'] = projectid
        initial['projectname'] = project.projectname
        initial['expertid'] = expertid
        initial['expertname'] = expert.expertname
        return initial

class ViewReviewResultView(forms.ModalFormView):
    template_name = 'admin/projectmgmt/viewreviewresult.html'
    form_id = 'viewreviewresult'
    form_class = project_forms.ViewReviewResultForm
    submit_label = ""
    cancel_label = u"放弃"
    modal_header = u"专家评审意见"
    success_url = 'horizon:admin:projectmgmt:managereviewresult'
    page_title = u"查看专家评审意见"
    policy_rules = (("expertreview", "expertreview:view:viewreviewresult"),)

    def get_success_url(self):
        return reverse(self.success_url,
                       args=(self.kwargs['projectid'],))

    @check_project_state(['start_review', 'finished'])
    def get_initial(self):
        initial = super(ViewReviewResultView, self).get_initial()
        projectid = self.kwargs['projectid']
        expertid = self.kwargs['expertid']
        project = project_db_handle.GetProjectInstanceById(projectid)
        expert = expert_db_handle.GetExpertInstanceById(expertid)
        initial['projectid'] = projectid
        initial['projectname'] = project.projectname
        initial['expertid'] = expertid
        initial['expertname'] = expert.expertname
        reviewer = project_db_handle.GetReviewerInstanceById(project, expertid,
                                           project_expected_states=['start_review', 'finished'],
                                           reviewer_expected_states=[REVIEWER_SELECTED])
        initial['comments'] = reviewer.comments
        initial['comments_attachments'] = reviewer.comments_attachments
        initial['comments_on_comments'] = reviewer.comments_on_comments
        return initial

