# -*- coding:utf-8 -*-

import logging
from datetime import datetime, date
from django.core.urlresolvers import NoReverseMatch
from django.core.urlresolvers import reverse
from django import shortcuts

from horizon import tables
from horizon import messages
from horizon import exceptions
from horizon.utils import filters

from openstack_dashboard.models import REVIEW_STATE_CHOICE
from openstack_dashboard.models import REVIEW_STATE_ONGOING
from openstack_dashboard.models import REVIEW_STATE_NOTSTART
from openstack_dashboard.models import REVIEW_STATE_COMMITTED
from openstack_dashboard.utils import expert_db_handle
from openstack_dashboard.utils import project_db_handle

from openstack_dashboard.dashboards.admin.projectmgmt import tables as projectmgmt_tables

LOG = logging.getLogger(__name__)

def date_in_CHN(d):
    if not d or not isinstance(d, (datetime, date)):
        return u"-"
    return "%04d-%02d-%02d" % (d.year, d.month, d.day)

def pingshengshijian_in_CHN(project):
    return date_in_CHN(project.pingshengshijian)

def disableAction(classes):
    if 'disabled' not in classes:
        classes = [c for c in classes] + ['disabled']
    return classes

def translate_review_state(project):
    if project.review_state in REVIEW_STATE_CHOICE:
        return REVIEW_STATE_CHOICE[project.review_state]
    else:
        return u"错误状态"

class UpdateReviewContent(tables.LinkAction):
    name = 'update_review_content'
    verbose_name = u"修改评审内容"
    classes = ("ajax-modal",)
    url = "horizon:project:review:updatereview"
    icon = "edit"
    policy_rules = (("expertreview", "expertreview:actions:update_review_content"),)

    def allowed(self, request, project):
        if project.state == 'start_review' \
            and project.review_state in [REVIEW_STATE_ONGOING, REVIEW_STATE_COMMITTED]:
            if project.review_state == REVIEW_STATE_COMMITTED:
                self.classes = disableAction(self.classes)
            return True
        return False

class FillReviewContent(tables.LinkAction):
    name = 'fill_review_content'
    verbose_name = u"填写评审内容"
    url = "horizon:project:review:doreview"
    icon = "edit"
    policy_rules = (("expertreview", "expertreview:actions:fill_review_content"),)

    def allowed(self, request, project):
        if project.state == 'start_review' \
            and project.review_state == REVIEW_STATE_NOTSTART:
            return True
        return False

class ViewReviewContent(tables.LinkAction):
    name = 'view_review_content'
    verbose_name = u"查看评审内容"
    url = "horizon:project:review:viewreview"
    icon = "edit"
    classes = ("ajax-modal",)
    policy_rules = (("expertreview", "expertreview:actions:view_review_content"),)

    def allowed(self, request, project):
        if project.review_state == REVIEW_STATE_NOTSTART:
            return False
        if project.state not in ['start_review', 'finished']:
            return False
        return True

class CommitReview(tables.BatchAction):
    name = 'submit_review_comment'
    classes = ("btn-suspend",)
    policy_rules = (("expertreview", "expertreview:actions:submit_review_comment"),)

    @staticmethod
    def action_present(count):
        return (u"提交评审结果",)

    @staticmethod
    def action_past(count):
        return (u"评审结果已提交",)

    def allowed(self, request, project=None):
        if not project:
            return False
        if project.state == 'start_review' \
            and project.review_state == REVIEW_STATE_ONGOING:
            return True
        return False

    def action(self, request, obj_id):
        redirect = reverse("horizon:settings:user:index")
        expertid = expert_db_handle.get_expertid_from_keystone_user(
            request, redirect=redirect)
        try:
            project_db_handle.CommitReviewResult(obj_id, expertid)
        except Exception as e:
            exceptions.handle(request, e.message, redirect=redirect)

class ReviewTable(projectmgmt_tables.BaseTable):
    pingshengshijian = tables.Column(pingshengshijian_in_CHN, verbose_name=u"项目评审或验收时间")
    pingshengdidian = tables.Column('pingshengdidian', verbose_name=u"项目评审或验收地点")
    review_state = tables.Column(translate_review_state, verbose_name=u"评审状态")
    class Meta(object):
        name = 'review_project_table'
        verbose_name = u"待评审项目列表"
        row_actions = (ViewReviewContent, FillReviewContent, UpdateReviewContent, CommitReview)
        policy_rules = (("expertreview", "expertreview:table:review_project_table"),)
