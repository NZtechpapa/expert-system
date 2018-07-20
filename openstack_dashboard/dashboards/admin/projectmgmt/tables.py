# -*- coding:utf-8 -*-
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

import logging
from datetime import datetime, date
from django.core.urlresolvers import NoReverseMatch
from django.core.urlresolvers import reverse
from django.http import QueryDict
from django import shortcuts
from django.utils.timesince import timesince
from django.template import defaultfilters as django_filters


from horizon import tables
from horizon import messages
from horizon import forms
from horizon.utils import filters

from openstack_dashboard.utils import expert_db_handle
from openstack_dashboard.utils import project_db_handle
from openstack_dashboard.utils import sendmessages
from openstack_dashboard.models import REVIEW_STATE_CHOICE
from openstack_dashboard.models import REVIEW_STATE_COMMITTED
from openstack_dashboard.models import Project

from openstack_dashboard.dashboards.admin.expertmgmt import tables as expertmgmt_tables

LOG = logging.getLogger(__name__)

def action_check_project_state(expected_states):
    def wrapper1(func):
        def wrapper2(self, *args, **kwargs):
            project = self.table.kwargs.get('project', None)
            if not project or not isinstance(project, Project):
                projectid = self.table.kwargs.get('projectid', None)
                if not projectid:
                    return False
                project = project_db_handle.GetProjectInstanceById(projectid)
                self.table.kwargs['project'] = project
            if not project or not project.state in expected_states:
                return False
            return func(self, *args, **kwargs)
        return wrapper2
    return wrapper1

def dict_to_set(dict_obj):
    rst = set()
    for k in dict_obj:
        rst.add( (k, "%s=" % dict_obj[k], True) )
    return rst

FILTER_CHOICES = dict_to_set(project_db_handle.SEARCHFIELDS_VALUE)

def translate_state(project):
    if project.state in project_db_handle.STATEMAPPING:
        return project_db_handle.STATEMAPPING[project.state]
    else:
        return project.state

def date_in_CHN(d):
    if not d or not isinstance(d, (datetime, date)):
        return u"-"
    return "%04d-%02d-%02d" % (d.year, d.month, d.day)

def shenbaoriqi_in_CHN(project):
    return date_in_CHN(project.shenbaoriqi)

def pingshengshijian_in_CHN(project):
    return date_in_CHN(project.pingshengshijian)

def get_candidates(project):
    return len(project_db_handle.GetAvailableCandidate(project, need_reviewer_info=False))

def get_reviewers(project):
    return len(project_db_handle.GetBindedReviewers(project, need_reviewer_info=False))

def calculate_time_since(project):
    return project.updated_at.isoformat()

def get_isPrioritized(expert):
    if expert.isPrioritized:
        return u"是"
    else:
        return u"否"

def get_isnotified(expert):
    if expert.isnotified:
        return u"是"
    else:
        return u"否"

def get_review_state(expert):
    if expert.review_state in REVIEW_STATE_CHOICE:
        return REVIEW_STATE_CHOICE[expert.review_state]
    else:
        return u"未知"

def disableAction(classes):
    if 'disabled' not in classes:
        classes = [c for c in classes] + ['disabled']
    return classes

class QuickGetAction(object):
    def quick_get_other_col_data(self, name, datum):
        _col = self.table.columns[name]
        datum_id = self.table.get_object_id(datum)
        if datum_id in self.table._data_cache[_col]:
            return self.table._data_cache[_col][datum_id]
        else:
            return _col.get_raw_data(datum)

# 搜索项目按键，在项目列表上
class SearchProjectAction(tables.LinkAction):
    name = 'searchproject'
    verbose_name = u"高级搜索"
    icon = "search"
    classes = ("ajax-modal",)
    tmp_url = "horizon:admin:projectmgmt:searchproject"
    policy_rules = (("expertreview", "expertreview:actions:searchproject"),)

    def get_link_url(self, project=None):
        user_data = project_db_handle.get_initial_user_data(self.table.request.GET, default=True)
        q = QueryDict('', mutable=True)
        for key in ['field1', 'oper1', 'field2', 'oper2', 'value1', 'value2', 'mainop']:
            if key in user_data:
                q[key] = user_data[key]
        redirect = reverse(self.tmp_url)
        return ('%s?%s' % (redirect, q.urlencode()))

# 过滤项目按键，在项目列表上
class FilterProjectAction(tables.FilterAction):
    name = 'filterproject'
    verbose_name = u"快速搜索"
    filter_type = "server"
    filter_choices = FILTER_CHOICES
    policy_rules = (("expertreview", "expertreview:actions:filterproject"),)

# 创建项目按键，在项目列表上
class CreateProjectAction(tables.LinkAction):
    name = 'createproject'
    verbose_name = u"录入项目信息"
    url = "horizon:admin:projectmgmt:createproject"
    classes = ("ajax-modal",)
    icon = "plus"
    policy_rules = (("expertreview", "expertreview:actions:createproject"),)

# 查看项目详情按键，在每个项目右边
class ViewProjectAction(tables.LinkAction):
    name = 'viewproject'
    verbose_name = u"查看"
    url = "horizon:admin:projectmgmt:viewproject"
    classes = ("ajax-modal",)
    icon = "plus"
    policy_rules = (("expertreview", "expertreview:actions:viewproject"),)

# 更新项目按键，在每个项目右边
class UpdateProjectAction(tables.LinkAction):
    name = 'updateproject'
    verbose_name = u"修改"
    classes = ("ajax-modal",)
    url = "horizon:admin:projectmgmt:updateproject"
    icon = "edit"
    policy_rules = (("expertreview", "expertreview:actions:updateproject"),)

    def allowed(self, request, project):
        return project.state == 'draft'

# 提交项目（召回申请）按键，在每个项目右边
class SubmitProjectAction(tables.BatchAction):
    name = 'submitproject'
    classes = ("btn-suspend",)
    policy_rules = (("expertreview", "expertreview:actions:submitproject"),)

    @staticmethod
    def action_present(count):
        return (u"提交审核",
                u"召回申请",)

    @staticmethod
    def action_past(count):
        return (u"已提交，等待审核",
                u"已召回，请修改后提交",)

    def allowed(self, request, project=None):
        if not project:
            return False
        if project.state == 'draft':
            self.submit = True
            self.current_present_action = 0
        elif project.state == 'waitfor_approve':
            self.submit = False
            self.current_present_action = 1
        else:
            return False
        return True

    def action(self, request, obj_id):
        if self.submit:
            project_db_handle.SubmitProjectInfo(obj_id)
            self.current_past_action = 0
        else:
            project_db_handle.WithdrawProjectReq(obj_id)
            self.current_past_action = 1

# 批准项目，在每个项目右边
class ApproveProjectAction(tables.BatchAction):
    name = 'approveproject'
    classes = ("btn-suspend",)
    policy_rules = (("expertreview", "expertreview:actions:approveproject"),)

    @staticmethod
    def action_present(count):
        return (u"批准项目",)

    @staticmethod
    def action_past(count):
        return (u"项目已批准",)

    def allowed(self, request, project=None):
        if not project:
            return False
        if project.state != 'waitfor_approve':
            return False
        return True

    def action(self, request, obj_id):
        project_db_handle.ApproveProjectReq(obj_id)
        return True


# 退回修改按键，在每个项目右边
class RejectProjectAction(tables.BatchAction):
    name = 'rejectproject'
    classes = ("btn-suspend",)
    policy_rules = (("expertreview", "expertreview:actions:rejectproject"),)

    @staticmethod
    def action_present(count):
        return (u"退回修改",)

    @staticmethod
    def action_past(count):
        return (u"已退回，等待修改后重新提交",)

    def allowed(self, request, project=None):
        if not project:
            return False
        if project.state != 'waitfor_approve':
            return False
        return True

    def action(self, request, obj_id):
        project_db_handle.RejectProjectReq(obj_id)


# 设置抽取规则，在每个项目的右侧
class SetRuleAction(tables.LinkAction):
    name = 'setrule'
    verbose_name = u"设置抽取规则"
    classes = ("ajax-modal",)
    url = "horizon:admin:projectmgmt:setrule"
    icon = "edit"
    policy_rules = (("expertreview", "expertreview:actions:setrule"),)

    def allowed(self, request, project=None):
        if not project.state == 'waitfor_setrule':
            return False
        return True

# 通知已被抽取的专家按钮，在每个项目右侧
class NotifyAllReviewers(tables.BatchAction):
    name = 'notifyall'
    classes = ("btn-suspend",)
    policy_rules = (("expertreview", "expertreview:actions:notifyall"),)

    @staticmethod
    def action_present(count):
        return (u"通知所有专家",)

    @staticmethod
    def action_past(count):
        return (u"通知已发送",)

    def allowed(self, request, project=None):
        if not project:
            return False
        if project.state != 'binded':
            return False
        return True

    def action(self, request, projectid):
        experts = project_db_handle.GetBindedReviewers(projectid, need_reviewer_info=False)
        project_dict = project_db_handle.GetProjectInstanceById(projectid, returnDict=True)
        for expert in experts:
            expert_db_handle.notify_expert(expert, sendmessages.TEMPLATE_NOTIFY_REVIEW_PROJECT,
                                           project_info=project_dict)
        project_db_handle.NotifiedReviewers(projectid, experts)
        return True

# 通知补抽的专家按钮，在每个项目右侧
class NotifyNewReviewers(tables.BatchAction):
    name = 'notifynew'
    classes = ("btn-suspend",)
    policy_rules = (("expertreview", "expertreview:actions:notifynew"),)

    @staticmethod
    def action_present(count):
        return (u"通知新抽取专家",)

    @staticmethod
    def action_past(count):
        return (u"通知已发送",)

    def allowed(self, request, project=None):
        if not project:
            return False
        if project.state != 'binded':
            return False
        experts = project_db_handle.GetNonNotifiedReviewers(project)
        if len(experts) == 0:
            #self.classes = disableAction(self.classes)
            return False
        return True

    def action(self, request, projectid):
        experts = project_db_handle.GetNonNotifiedReviewers(projectid)
        project_dict = project_db_handle.GetProjectInstanceById(projectid, returnDict=True)
        for expert in experts:
            expert_db_handle.notify_expert(expert, sendmessages.TEMPLATE_NOTIFY_REVIEW_PROJECT,
                                           project_info=project_dict)
        project_db_handle.NotifiedReviewers(projectid, experts)
        return True

# 启动项目以及完成评审按钮，在每个项目的右侧
class ProjectKickoff(tables.BatchAction):
    name = 'kickoff'
    classes = ("btn-suspend",)
    policy_rules = (("expertreview", "expertreview:actions:kickoffproject"),)

    @staticmethod
    def action_present(count):
        return (u"生成项目档案",
                u"完成评审",)

    @staticmethod
    def action_past(count):
        return (u"项目档案已生成，等待启动项目评审",
                u"项目评审已完成",)

    def allowed(self, request, project=None):
        if not project:
            return False
        if project.state == 'binded':
            self.current_present_action = 0
            self.kickoff = True
        elif project.state == 'start_review':
            self.current_present_action = 1
            self.kickoff = False
            if not project_db_handle.AllReviewSubmitted(project):
                #self.classes = disableAction(self.classes)
                return False
        else:
            return False
        return True

    def action(self, request, obj_id):
        if self.kickoff:
            project_db_handle.ProjectFinishCurrentBind(obj_id)
            project_db_handle.KickoffProject(obj_id)
            self.current_past_action = 0
        else:
            project_db_handle.FinishReviewProject(obj_id)
            self.current_past_action = 1

# 管理候选专家池，在每个项目的右侧
class ManageCandidate2Action(tables.LinkAction):
    name = 'managecandidate2'
    verbose_name = u"管理候选专家（超管专用）"
    url = "horizon:admin:projectmgmt:managecandidate2"
    icon = "edit"
    policy_rules = (("expertreview", "expertreview:actions:managecandidate2"),)

    def allowed(self, request, project):
        if not project.state == 'waitfor_bind':
            return False
        return True

# 管理候选专家池，在每个项目的右侧
class ManageCandidateAction(tables.LinkAction):
    name = 'managecandidate'
    verbose_name = u"管理候选专家"
    url = "horizon:admin:projectmgmt:managecandidate"
    icon = "edit"
    policy_rules = (("expertreview", "expertreview:actions:managecandidate"),)

    def allowed(self, request, project):
        if not project.state == 'waitfor_bind':
            return False
        return True

# 随机抽取专家，在每个项目的右侧
class RandomBindReviewerAction(tables.LinkAction, QuickGetAction):
    name = 'randombind'
    verbose_name = u"随机抽取"
    url = "horizon:admin:projectmgmt:randombind"
    classes = ("ajax-modal",)
    icon = "edit"
    policy_rules = (("expertreview", "expertreview:actions:randombind"),)

    def allowed(self, request, project):
        if not project.state == 'waitfor_bind':
            return False
        candidates_num = self.quick_get_other_col_data('candidates_num', project)
        if not candidates_num:
            self.classes = disableAction(self.classes)
        return True

# 补抽评审专家，在每个项目的右侧
class AddtionalBindReviewerAction(tables.BatchAction, QuickGetAction):
    name = 'addtionalbind'
    icon = "edit"
    policy_rules = (("expertreview", "expertreview:actions:addtionalbind"),)

    @staticmethod
    def action_present(count):
        return (u"开始补充抽取",)

    @staticmethod
    def action_past(count):
        return (u"请点击“随机抽取”开始补抽",)

    def allowed(self, request, project):
        if not project.state == 'binded':
            return False
        chouqurenshu = project.chouqurenshu
        reviewers_num = self.quick_get_other_col_data('reviewers_num', project)
        if reviewers_num >= chouqurenshu:
            return False
        return True

    def action(self, request, obj_id):
        project_db_handle.AddtionalBindExperts(obj_id)
        return True

#管理评审专家，在每个项目的右侧
class ManageReviewerAction(tables.LinkAction):
    name = 'managereviewer'
    verbose_name = u"管理评审专家"
    url = "horizon:admin:projectmgmt:managereviewer"
    icon = "edit"
    policy_rules = (("expertreview", "expertreview:actions:managereviewer"),)

    def allowed(self, request, project):
        if not project.state in ['waitfor_bind', 'binded']:
            return False
        return True

#管理评审专家（超管专用），在每个项目的右侧
class ManageReviewer2Action(tables.LinkAction):
    name = 'managereviewer2'
    verbose_name = u"管理评审专家（超管专用）"
    url = "horizon:admin:projectmgmt:managereviewer2"
    icon = "edit"
    policy_rules = (("expertreview", "expertreview:actions:managereviewer2"),)

    def allowed(self, request, project):
        if not project.state in ['waitfor_setrule', 'waitfor_bind', 'binded']:
            return False
        return True

# 查看评审专家，抽取完成之后显示，在每个项目的右侧
class ViewReviewerAction(tables.LinkAction):
    name = 'viewreviewer'
    verbose_name = u"查看评审专家"
    url = "horizon:admin:projectmgmt:viewreviewer"
    icon = "edit"
    policy_rules = (("expertreview", "expertreview:actions:viewreviewer"),)

    def allowed(self, request, project):
        if not project.state in ['kickoff', 'start_review', 'finished']:
            return False
        return True

# 新一轮抽取，在每个项目的右侧
class SetNewRuleAction(tables.BatchAction, QuickGetAction):
    name = 'setnewrule'
    icon = "edit"
    policy_rules = (("expertreview", "expertreview:actions:setnewrule"),)

    @staticmethod
    def action_present(count):
        return (u"开始新一轮抽取",
                u"重新设置抽取规则")

    @staticmethod
    def action_past(count):
        return (u"请点击“设置抽取条件”开始新一轮的抽取",)

    def allowed(self, request, project):
        if not project.state in ['waitfor_bind', 'binded']:
            return False
        if project.state == 'waitfor_bind':
            candidates_num = self.quick_get_other_col_data('candidates_num', project)
            if candidates_num != 0:
                return False
            else:
                self.current_present_action = 1
        else:
            chouqurenshu = project.chouqurenshu
            reviewers_num = self.quick_get_other_col_data('reviewers_num', project)
            if reviewers_num >= chouqurenshu:
                return False
            else:
                self.current_present_action = 0
        return True

    def action(self, request, obj_id):
        project_db_handle.StartNewBind(obj_id)
        return True

# 强制重新设置抽取条件（超管专用）
class ForceSetNewRule2Action(tables.BatchAction):
    name = 'forcesetnewrule2'
    icon = "edit"
    policy_rules = (("expertreview", "expertreview:actions:forcesetnewrule2"),)

    @staticmethod
    def action_present(count):
        return (u"重新设置抽取规则（超管专用）", )

    @staticmethod
    def action_past(count):
        return (u"请点击“设置抽取条件”开始新一轮的抽取",)

    def allowed(self, request, project):
        if not project.state in ['waitfor_bind',]:
            return False
        self.current_present_action = 0
        return True

    def action(self, request, obj_id):
        project_db_handle.StartNewBind(obj_id)
        return True


# 项目启动评审按钮，在每个项目右侧
class ProjectStartReview(tables.LinkAction):
    name = 'startreview'
    verbose_name = u"启动项目评审"
    classes = ("ajax-modal",)
    url = "horizon:admin:projectmgmt:startreview"
    icon = "edit"
    policy_rules = (("expertreview", "expertreview:actions:startreview"),)

    def allowed(self, request, project):
        if not project.state == 'kickoff':
            return False
        return True

# 评审内容管理，在每个已完成评审的项目的右侧
class ManageReviewResultAction(tables.LinkAction):
    name = 'managereviewresult'
    verbose_name = u"评审管理"
    url = "horizon:admin:projectmgmt:managereviewresult"
    icon = "edit"
    policy_rules = (("expertreview", "expertreview:actions:managereviewresult"),)

    def allowed(self, request, project):
        if not project.state in ['start_review', 'finished']:
            return False
        return True

# 删除项目，在每个项目的右侧。
# 1，在draft，waitfor_approve状态下可以删除
# 2，在waitfor_setrule状态下，如果没有抽取过，也可以删除
# 3，在kickoff状态下，由于需求修改，已经变成不能删除
class ProjectDelete(tables.DeleteAction, QuickGetAction):
    help_text = u"删除项目"
    policy_rules = (("expertreview", "expertreview:actions:deleteproject"),)

    @staticmethod
    def action_present(count):
        return (u"删除项目",
                u"作废项目",)

    @staticmethod
    def action_past(count):
        return (u"已删除", u"账号删除失败，项目信息保留",)

    def allowed(self, request, project=None):
        if not project:
            return False
        if project.state in ['deleted', 'kickoff', 'binded', 'start_review', 'finished']:
            return False
        if project.state in ['waitfor_setrule', 'waitfor_bind']:
            reviewers_num = self.quick_get_other_col_data('reviewers_num', project)
            if reviewers_num:
                return False
            self.current_present_action = 1
        else:
            self.current_present_action = 0
        return True

    def action(self, request, obj_id):
        result = project_db_handle.DeleteProjectRecord(obj_id)
        self.current_past_action = 0 if result else 1

# Table
# 项目列表，BaseTable可供专家个人评审的界面重复使用
class BaseTable(tables.DataTable):
    id = tables.Column("id", verbose_name=u"项目序号", hidden=False)
    serial_no = tables.Column("serial_no", verbose_name=u"项目编号", hidden=True)
    projectname = tables.Column("projectname", verbose_name=u"项目名称")
    leibie = tables.Column("leibie", verbose_name=u"项目类别")
    shenbaoriqi = tables.Column(shenbaoriqi_in_CHN, verbose_name=u"项目申报日期")

    def get_object_display_key(self, datum):
        return 'projectname'

# Table
# 项目列表，额外项供管理员查看
class ProjectsTable(BaseTable):
    fuzeren = tables.Column("fuzeren", verbose_name=u"项目负责人")
    shenbaodanwei = tables.Column('shenbaodanwei', verbose_name=u"项目单位", hidden=True)
    yewuchushi = tables.Column("yewuchushi", verbose_name=u"业务处室")
    chouqurenshu = tables.Column("chouqurenshu", verbose_name=u"抽取人数")
    candidates_num = tables.Column(get_candidates, verbose_name=u"候选专家数量", hidden=True)
    reviewers_num = tables.Column(get_reviewers, verbose_name=u"已抽取人数", hidden=False)
    state = tables.Column(translate_state, verbose_name=u"项目状态")
    updated_at = tables.Column(calculate_time_since,
                               verbose_name=u"距上次更新",
                               filters=(filters.parse_isotime,
                                        filters.timesince_sortable),
                               attrs={'data-type': 'timesince'}, hidden=True)

    class Meta(object):
        name = 'projectstable'
        verbose_name = u"项目列表"
        table_actions = (FilterProjectAction, SearchProjectAction, CreateProjectAction,)
        row_actions = (ViewProjectAction, UpdateProjectAction, SubmitProjectAction, ApproveProjectAction,
                       RejectProjectAction, SetRuleAction, ManageCandidateAction, ManageCandidate2Action,
                       RandomBindReviewerAction, ManageReviewerAction, ManageReviewer2Action,
                       AddtionalBindReviewerAction, SetNewRuleAction, ProjectStartReview, ViewReviewerAction,
                       ManageReviewResultAction, NotifyAllReviewers, NotifyNewReviewers, ProjectKickoff,
                       ProjectDelete,)
        policy_rules = (("expertreview", "expertreview:table:projectstable"),)

#===============================================================
# 符合条件的候选人列表
# 根据搜索结果显示专家列表
#===============================================================
class SearchCandidate2Action(expertmgmt_tables.ExpertSearch):
    tmp_url = "horizon:admin:projectmgmt:searchcandidate2"
    policy_rules = (("expertreview", "expertreview:actions:searchcandidate2"),)

    def get_link_url(self, datum=None):
        args = (self.table.kwargs['projectid'],)
        self.redirect_url = reverse(self.tmp_url, args=args)
        return super(SearchCandidate2Action, self).get_link_url(datum=datum)

# 手动将指定专家加入候选池，在专家搜索结果列表，每个专家的右侧
class AddCandidate2Action(tables.BatchAction):
    name = 'addcandidate2'
    classes = ("btn-suspend",)
    help_text = u"添加为候选人"
    icon = "plus"
    policy_rules = (("expertreview", "expertreview:actions:addcandidate2"),)

    @staticmethod
    def action_present(count):
        return (u"添加为候选人",)

    @staticmethod
    def action_past(count):
        return (u"已添加为候选人",)

    def handle(self, table, request, obj_ids):
        projectid = table.kwargs['projectid']
        experts = []
        for expertid in obj_ids:
            expert = table.get_object_by_id(expertid)
            experts.append(expert)

        (project, has_in_pool, has_in_project, has_unavailable) = \
            project_db_handle.AddCandidates(projectid, experts)
        all_experts= []
        has_in_project_experts = []
        has_in_pool_experts = []
        has_unavailable_experts = []
        for expert in experts:
            if expert in has_in_project:
                has_in_project_experts.append(expert)
            elif expert in has_in_pool:
                has_in_pool_experts.append(expert)
            elif expert in has_unavailable:
                has_unavailable_experts.append(expert)
            else:
                all_experts.append(expert)

        if all_experts:
            names = expert_db_handle.get_all_expert_names(all_experts)
            messages.success(request, u"以下专家：%s，已加入项目%s的候选专家列表" %
                                      (names, project.projectname))
        if has_in_pool_experts:
            names = expert_db_handle.get_all_expert_names(has_in_pool_experts)
            messages.info(request, u"以下专家：%s，未加入项目%s的候选专家列表，原因：%s" %
                                   (names,
                                    project.projectname,
                                    u"已存在于候选专家列表中"))
        if has_unavailable_experts:
            names = expert_db_handle.get_all_expert_names(has_unavailable_experts)
            messages.info(request, u"以下专家：%s，未加入项目%s的候选专家列表，原因：%s" %
                                   (names,
                                    project.projectname,
                                    u"已从候选专家列表或评审专家列表中删除"))
        if has_in_project_experts:
            names = expert_db_handle.get_all_expert_names(has_in_project_experts)
            messages.error(request, u"以下专家：%s，未加入项目%s的候选专家列表，原因：%s" %
                                    (names,
                                     project.projectname,
                                     u"已参与该项目评审"))

        return shortcuts.redirect(self.get_success_url(request))

# Table
# 与候选专家列表配合，超级管理员专用
class MatchCandidate2Table(expertmgmt_tables.BaseTable):
    class Meta(object):
        name = 'matchcandidate2'
        verbose_name = u"专家搜索结果列表"
        table_actions = (AddCandidate2Action, SearchCandidate2Action,)
        row_actions = (expertmgmt_tables.ExpertDetail, AddCandidate2Action,)
        policy_rules = (("expertreview", "expertreview:table:matchcandidate2"),)


#===============================================================
# 候选专家列表
#===============================================================
# 将专家从候选列表中删除，管理候选列表中，每个专家的右侧
class DeleteCandidateAction(tables.DeleteAction):
    help_text = u"删除候选人"
    policy_rules = (("expertreview", "expertreview:actions:deletecandidate"),)

    @staticmethod
    def action_present(count):
        return u"删除候选人"

    @staticmethod
    def action_past(count):
        return u"候选人已删除"

    @action_check_project_state(['waitfor_bind'])
    def allowed(self, request, expert=None):
        return True

    def action(self, request, obj_id):
        projectid = self.table.kwargs['projectid']
        expert = self.table.get_object_by_id(obj_id)
        project_db_handle.RemoveCandidate(projectid, expert)

# 人为抽取指定专家，跳过随机抽取环节，超管专用
class ManualBind2Action(tables.BatchAction):
    name = 'manualbind2'
    classes = ("btn-suspend",)
    help_text = u"抽取该专家评审项目"
    icon = "plus"
    policy_rules = (("expertreview", "expertreview:actions:manualbind2"),)

    @staticmethod
    def action_present(count):
        if count == 1:
            return (u"加入评审",)
        else:
            return (u"指定加入评审",)

    @staticmethod
    def action_past(count):
        return (u"已加入项目评审",)

    def handle(self, table, request, obj_ids):
        projectid = table.kwargs['projectid']
        experts = []
        for expertid in obj_ids:
            expert = table.get_object_by_id(expertid)
            experts.append(expert)

        (project, not_in_pool, has_in_project) = \
            project_db_handle.AddExpertsIntoProject(projectid, experts)

        all_experts = []
        has_in_project_experts = []
        for expert in experts:
            if expert in has_in_project:
                has_in_project_experts.append(expert)
            else:
                all_experts.append(expert)

        if all_experts:
            names = expert_db_handle.get_all_expert_names(all_experts)
            messages.success(request, u"以下专家：%s，已加入项目%s的候选专家列表" %
                                      (names, project.projectname))
        if has_in_project_experts:
            names = expert_db_handle.get_all_expert_names(has_in_project_experts)
            messages.info(request, u"以下专家：%s，未加入项目%s为评审，原因：%s" %
                                   (names, project.projectname,
                                    u"已参与该项目评审"))
        return shortcuts.redirect(self.get_success_url(request))

# 设置专家被默认抽取，在专家管理页面，每个专家的右侧
class PrioritizeExpertAction(tables.BatchAction):
    name = 'prioritizeexpert'
    classes = ("btn-launch",)
    help_text = u"设置该专家被优先抽取"
    icon = "plus"
    policy_rules = (("expertreview", "expertreview:actions:prioritizeexpert"),)

    @staticmethod
    def action_present(count):
        return (u"设置被优先抽取",
                u"取消被优先抽取",)

    @staticmethod
    def action_past(count):
        return (u"已设置被优先抽取",
                u"已取消被优先抽取",)

    @action_check_project_state(['waitfor_bind'])
    def allowed(self, request, expert=None):
        if not expert:
            return False
        self.isPrioritized = expert.isPrioritized
        if not expert.isPrioritized:
            self.current_present_action = 0
        else:
            self.current_present_action = 1
        return True

    def action(self, request, expertid):
        projectid = self.table.kwargs['projectid']
        if not self.isPrioritized:
            project_db_handle.PrioritizeExpertInProject(projectid, expertid)
            self.current_past_action = 0
        else:
            project_db_handle.DeprioritizeExpertInProject(projectid, expertid)
            self.current_past_action = 1

# Table
# 1，设置隐藏专家（取消设置）
# 2，手动抽取指定专家（超级管理员专用）
# 3，从列表中删除指定专家
class CandidateTable(expertmgmt_tables.BaseTable):
    isPrioritized = tables.Column(get_isPrioritized, verbose_name=u"是否优先抽取")
    class Meta(object):
        name = 'candidatetable'
        verbose_name = u"候选专家列表"
        table_actions = (ManualBind2Action, DeleteCandidateAction,)
        row_actions = (expertmgmt_tables.ExpertDetail, ManualBind2Action,
                       PrioritizeExpertAction, DeleteCandidateAction,)
        policy_rules = (("expertreview", "expertreview:table:candidatetable"),)


#===============================================================
# 管理已抽取评审专家
#===============================================================
class NotifyBaseAction(tables.BatchAction):
    classes = ("btn-suspend",)

    @staticmethod
    def action_present(count):
        pass

    @staticmethod
    def action_past(count):
        pass

    @action_check_project_state(['waitfor_setrule', 'waitfor_bind', 'binded'])
    def allowed(self, request, expertid):
        return True

    def do_notify(self, expertid):
        projectid = self.table.kwargs['projectid']
        project_dict = project_db_handle.GetProjectInstanceById(projectid, returnDict=True)
        expert_db_handle.notify_expert(expertid, sendmessages.TEMPLATE_NOTIFY_REVIEW_PROJECT,
                                       project_info=project_dict)

    def set_notified(self, expertid):
        projectid = self.table.kwargs['projectid']
        project_db_handle.NotifiedReviewers(projectid, [expertid])

# 标记为已通知
class SetNotifiedAction(NotifyBaseAction):
    name = 'setnotified'
    policy_rules = (("expertreview", "expertreview:actions:setnotified"),)

    @staticmethod
    def action_present(count):
        return (u"标记为已通知",)

    @staticmethod
    def action_past(count):
        return (u"已标记",)

    def action(self, request, expertid):
        self.set_notified(expertid)

# 通知专家，每个专家的右侧
class NotifyReviewerAction(NotifyBaseAction):
    name = 'notifyreviewer'
    policy_rules = (("expertreview", "expertreview:actions:notifyreviewer"),)

    @staticmethod
    def action_present(count):
        return (u"发送通知",)

    @staticmethod
    def action_past(count):
        return (u"通知已发送",)

    def action(self, request, expertid):
        self.do_notify(expertid)
        self.set_notified(expertid)

# 将专家从已抽取的评审列表中删除，管理评审列表中，每个专家的右侧
class RemoveReviewerAction(tables.DeleteAction):
    help_text = u"从评审列表中删除"
    policy_rules = (("expertreview", "expertreview:actions:removereviewer"),)

    @staticmethod
    def action_present(count):
        return u"从评审列表中删除"

    @staticmethod
    def action_past(count):
        return u"已从评审列表中删除"

    @action_check_project_state(['waitfor_bind', 'binded'])
    def allowed(self, request, expertid):
        return True

    def action(self, request, obj_id):
        projectid = self.table.kwargs['projectid']
        expert = self.table.get_object_by_id(obj_id)
        project_db_handle.RemoveExpertFromProject(projectid, expert)


# Table
# 管理评审专家列表
# 1, 从列表中删除指定专家
class ReviewerTable(expertmgmt_tables.BaseTable):
    isnotified = tables.Column(get_isnotified, verbose_name=u"是否被通知过")

    class Meta(object):
        name = 'reviewertable'
        verbose_name = u"评审专家列表"
        table_actions = (NotifyReviewerAction, SetNotifiedAction, RemoveReviewerAction,)
        row_actions = (expertmgmt_tables.ExpertDetail, NotifyReviewerAction, 
                       SetNotifiedAction, RemoveReviewerAction,)
        policy_rules = (("expertreview", "expertreview:table:reviewertable"),)


#===============================================================
# 管理无法参与的评审专家（超管专用）
#===============================================================
# 恢复无法参与评审专家
class RevertUnavailableReviewerAction2(tables.BatchAction):
    name = 'revertunavailablerevieweraction2'
    classes = ("btn-suspend",)
    help_text = u"恢复参与评审"
    icon = "plus"
    policy_rules = (("expertreview", "expertreview:actions:revertunavailablerevieweraction2"),)

    @staticmethod
    def action_present(count):
        return (u"恢复参与评审",)

    @staticmethod
    def action_past(count):
        return (u"已恢复参与评审之资格",)

    def action(self, request, obj_id):
        projectid = self.table.kwargs['projectid']
        expert = self.table.get_object_by_id(obj_id)
        project_db_handle.RevertUnavailableReviewer(projectid, expert)

# Table
# 无法参与评审之专家列表
class UnavailableReviewerTable(expertmgmt_tables.BaseTable):
    class Meta(object):
        name = 'unavailablereviewertable'
        verbose_name = u"无法参与评审之专家列表"
        table_actions = (RevertUnavailableReviewerAction2,)
        row_actions = (expertmgmt_tables.ExpertDetail,
                       RevertUnavailableReviewerAction2,)
        policy_rules = (("expertreview", "expertreview:table:unavailablereviewertable"),)

#===============================================================
# 管理评审结果列表
#===============================================================
# 查看评审结果，在每个评审专家的右侧
class ViewReviewResultAction(tables.LinkAction):
    name = 'viewreviewresult'
    verbose_name = u"查看评审内容"
    classes = ("ajax-modal",)
    tmp_url = "horizon:admin:projectmgmt:viewreviewresult"
    icon = 'view'
    policy_rules = (("expertreview", "expertreview:actions:viewreviewresult"),)

    def get_link_url(self, expert=None):
        args = (self.table.kwargs['projectid'], expert.id,)
        return reverse(self.tmp_url, args=args)

    @action_check_project_state(['start_review', 'finished'])
    def allowed(self, request, expert):
        if expert.review_state != REVIEW_STATE_COMMITTED:
            self.classes = disableAction(self.classes)
        return True

# 强制提交按钮，在每个评审专家的右侧
class ForceSubmitReviewResultAction(tables.BatchAction):
    name = 'forcesubmitreviewresult'
    classes = ("btn-suspend",)
    verbose_name = u"强制提交"
    policy_rules = (("expertreview", "expertreview:actions:forcesubmitreviewresult"),)

    @staticmethod
    def action_present(count):
        return (u"退回修改",
                u"强制提交",)

    @staticmethod
    def action_past(count):
        return (u"已强制提交，所有评审提交后方可结束项目",)

    @action_check_project_state(['start_review'])
    def allowed(self, request, expert):
        if expert.review_state == REVIEW_STATE_COMMITTED:
            self.current_present_action = 0
            self.isSubmit = False
        else:
            self.current_present_action = 1
            self.isSubmit = True
        return True

    def action(self, request, expertid):
        projectid = self.table.kwargs['projectid']
        if self.isSubmit:
            project_db_handle.ForceCommitReviewResult(projectid, expertid)
        else:
            project_db_handle.ReturnReviewResult(projectid, expertid)
        return True

# 评价专家评审结果，在每个评审专家的右侧
class CommentReviewResultAction(tables.LinkAction):
    name = 'commentreviewresult'
    verbose_name = u"评论专家评审意见"
    classes = ("ajax-modal",)
    tmp_url = "horizon:admin:projectmgmt:commentreviewresult"
    icon = 'edit'
    policy_rules = (("expertreview", "expertreview:actions:commentreviewresult"),)

    def get_link_url(self, expert=None):
        args = (self.table.kwargs['projectid'], expert.id,)
        return reverse(self.tmp_url, args=args)

    @action_check_project_state(['finished'])
    def allowed(self, request, expert):
        return True

# Table
# 评审结果管理列表
class ManageReviewResultTable(expertmgmt_tables.BaseTable):
    review_state = tables.Column(get_review_state, verbose_name=u"评审状态")
    class Meta(object):
        name = 'managereviewresult'
        verbose_name = u"评审结果列表"
        row_actions = (expertmgmt_tables.ExpertDetail, ViewReviewResultAction,
                       ForceSubmitReviewResultAction, CommentReviewResultAction,)
        policy_rules = (("expertreview", "expertreview:table:managereviewresult"),)

