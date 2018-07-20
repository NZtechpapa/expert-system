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
from datetime import date

from django import template
from django.conf import settings
from django.core.urlresolvers import NoReverseMatch
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.http import QueryDict
from django.utils.timesince import timesince
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import messages
from horizon import tables
from horizon.utils import filters

from openstack_dashboard import api
from openstack_dashboard.utils import expert_db_handle
from openstack_dashboard.utils import keystone_handler

LOG = logging.getLogger(__name__)

def dict_to_set(dict_obj):
    rst = set()
    for k in dict_obj:
        rst.add( (k, "%s=" % dict_obj[k], True) )
    return rst

FILTER_CHOICES = dict_to_set(expert_db_handle.SEARCHFIELDS_VALUE)

def keystone_create_account(request, expert):
    if not expert.keystone_username:
        return None
    if not expert.keystone_initial_pwd:
        return None
    domain = api.keystone.get_default_domain(request, False)
    try:
        description = "Account for expert %s(%d)" % (expert.expertname, expert.id)
        return keystone_handler.api_user_create(request, expert.id, expert.keystone_username,
                                                expert.keystone_initial_pwd, expert.email,
                                                description)
    except exceptions.Conflict:
        msg = _('User name "%s" is already used.') % expert.keystone_username
        messages.error(request, msg)
        return None
    except Exception:
        exceptions.handle(request, _('Unable to create user.'))
        return None

def keystone_approve_expert(request, expert):
    uid = expert.keystone_uuid
    if not uid:
        new_expert = keystone_create_account(request, expert)
        if not new_expert:
            return False
        uid = new_expert.id
        result = expert_db_handle.AccountCreated(expert, new_expert)
        if not result:
            keystone_handler.user_delete(request, uid)
            return False
    try:
        keystone_handler.api_grant_role(request, uid,
                                        rolename=settings.EXPERTCONSTANT['expert_certified_role'])
        return True
    except Exception:
        exceptions.handle(request, u"无法批准专家资料")
        return False

def keystone_delete_account(request, expert):
    uid = expert.keystone_uuid
    if not uid:
        return True
    try:
        keystone_handler.user_delete(request, uid)
        return True
    except Exception:
        exceptions.handle(request, u"无法删除专家账号%s" % uid)
        return False

class ExpertSearch(tables.LinkAction):
    name = "search_expert"
    verbose_name = u"高级搜索"
    icon = "search"
    classes = ("ajax-modal",)
    redirect_url = reverse_lazy("horizon:admin:expertmgmt:search")
    policy_rules = (("expertreview", "expertreview:actions:searchexpert"),)

    def get_link_url(self, datum=None):
        user_data = expert_db_handle.get_initial_user_data(self.table.request.GET, default=True)
        q = QueryDict('', mutable=True)
        for key in ['field1', 'oper1', 'field2', 'oper2', 'value1', 'value2', 'mainop']:
            if key in user_data:
                q[key] = user_data[key]
        return ('%s?%s' % (self.redirect_url, q.urlencode()))

def translate_state(expert):
    if expert.state in expert_db_handle.STATEMAPPING:
        return expert_db_handle.STATEMAPPING[expert.state]
    else:
        return expert.state

class ExpertFilter(tables.FilterAction):
    name = 'expert_filter'
    verbose_name = u"快速搜索"
    filter_type = "server"
    filter_choices = FILTER_CHOICES
    needs_preloading = False
    policy_rules = (("expertreview", "expertreview:actions:filterexpert"),)

class ExpertDetail(tables.LinkAction):
    name = "detail"
    verbose_name = u"查看"
    url = "horizon:admin:expertmgmt:detail"
    classes = ("ajax-modal",)
    icon = "plus"
    policy_rules = (("expertreview", "expertreview:actions:viewexpert"),)

class ExpertCreate(tables.LinkAction):
    name = "create"
    verbose_name = u"录入专家信息"
    url = "horizon:admin:expertmgmt:create"
    classes = ("ajax-modal",)
    icon = "plus"
    policy_rules = (("expertreview", "expertreview:actions:createexpert"),)

class ExpertUpdate(tables.LinkAction):
    name = "update"
    verbose_name = u"修改"
    classes = ("ajax-modal",)
    url = "horizon:admin:expertmgmt:update"
    icon = "edit"
    policy_rules = (("expertreview", "expertreview:actions:editexpert"),)

    def allowed(self, request, datum):
        return datum.state == 'draft'

class ExpertSubmit(tables.BatchAction):
    name = "submit"
    classes = ("btn-suspend",)
    policy_rules = (("expertreview", "expertreview:actions:submitexpert"),)

    @staticmethod
    def action_present(count):
        return (u"提交审核",
                u"召回申请",)

    @staticmethod
    def action_past(count):
        return (u"已提交，等待审核",
                u"已召回，请修改后提交",
                u"数据库出错",)

    def allowed(self, request, expert=None):
        if not expert:
            return False
        if expert.state == 'draft':
            self.submit = True
            self.current_present_action = 0
        elif expert.state in ['waitfor_check', ]:
            self.submit = False
            self.current_present_action = 1
        else:
            return False
        # Add more check later
        return True

    def action(self, request, obj_id):
        if self.submit:
            result = expert_db_handle.SubmitExpertInfo(obj_id)
            self.current_past_action = 0
        else:
            result = expert_db_handle.WithdrawExpertReq(obj_id)
            self.current_past_action = 1
        if not result:
            self.current_past_action = 2

class ExpertCheckReject(tables.BatchAction):
    name = "reject"
    classes = ("btn-suspend",)
    policy_rules = (("expertreview", "expertreview:actions:rejectexpert"),)

    @staticmethod
    def action_present(count):
        return (u"退回修改",)

    @staticmethod
    def action_past(count):
        return (u"已退回修改，等待再次提交",)

    def allowed(self, request, expert=None):
        if not expert:
            return False
        if expert.state in ['waitfor_check', 'approved',]:
            self.nextstep = 'reject'
            self.current_present_action = 0
        else:
            return False
        return True

    def action(self, request, obj_id):
        if self.nextstep == 'reject':
            expert_db_handle.WithdrawExpertReq(obj_id)
            self.current_past_action = 0
        return True

class ExpertCreateAccount(tables.BatchAction):
    name = "create_account"
    classes = ("btn-suspend",)
    policy_rules = (("expertreview", "expertreview:actions:createaccount"),)

    @staticmethod
    def action_present(count):
        return (u"创建账号",)

    @staticmethod
    def action_past(count):
        return (u"账号已创建",
                u"数据库出错",)

    def allowed(self, request, expert=None):
        if not expert:
            return False
        if expert.keystone_uuid:
            return False
        if expert.state not in ['draft',]:
            return False
        self.current_present_action = 0
        return True

    def action(self, request, obj_id):
        self.current_past_action = 1
        expert = expert_db_handle.GetExpertInstanceById(obj_id)
        if not expert:
            return
        new_user = keystone_create_account(request, expert)
        if not new_user:
            return
        result = expert_db_handle.AccountCreated(expert, new_user)
        if result:
            self.current_past_action = 0

class ExpertCheck(tables.BatchAction):
    name = "check"
    classes = ("btn-suspend",)
    policy_rules = (("expertreview", "expertreview:actions:approveexpert"),)

    @staticmethod
    def action_present(count):
        return (u"确认核实批准",)

    @staticmethod
    def action_past(count):
        return (u"已批准，等待创建账号",
                u"数据库出错",)

    def allowed(self, request, expert=None):
        if not expert:
            return False
        if expert.state != 'waitfor_check':
            return False
        self.current_present_action = 0
        return True

    def action(self, request, obj_id):
        self.current_past_action = 1
        expert = expert_db_handle.GetExpertInstanceById(obj_id)
        if not expert:
            return
        result = keystone_approve_expert(request, expert)
        if result:
            result = expert_db_handle.CheckExpertInfo(expert)
        if result:
            self.current_past_action = 0

class ExpertDelete(tables.DeleteAction):
    help_text = u"删除专家"
    policy_rules = (("expertreview", "expertreview:actions:deleteexpert"),)

    @staticmethod
    def action_present(count):
        return u"删除专家信息"

    @staticmethod
    def action_past(count):
        return (u"已删除", u"账号删除失败，专家信息保留",)

    def allowed(self, request, expert=None):
        if not expert:
            return False
        if expert.state in ['deleted', ]:
            return False
        return True

    def action(self, request, obj_id):
        self.current_past_action = 1
        expert = expert_db_handle.GetExpertInstanceById(obj_id)
        if not expert:
            return
        result = keystone_delete_account(request, expert)
        if not result:
            return
        result = expert_db_handle.DeleteExpertRecord(expert)
        if result:
            self.current_past_action = 0

def get_age(expert):
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

def calculate_time_since(expert):
    return expert.updated_at.isoformat()

def get_expert_domains(expert):
    domains = expert_db_handle.GetAllExpertDomain(expert)
    template_name = 'admin/expertmgmt/_expert_domains.html'
    domain_names = [ d.domainname for d in domains ]
    context = {
        'domain_names': domain_names
    }
    return template.loader.render_to_string(template_name, context)

class BaseTable(tables.DataTable):
    id = tables.Column("id", verbose_name="ID", hidden=True)
    expertname = tables.Column("expertname", verbose_name=u"姓名")
    age = tables.Column(get_age, verbose_name=u"年龄")
    zhicheng = tables.Column('zhicheng', verbose_name=u"职称")
    suozaidaiwen = tables.Column('suozaidaiwei', verbose_name=u"所在单位")
    email = tables.Column("email", verbose_name=u"邮箱")
    zuigaoxueli = tables.Column("zuigaoxueli", verbose_name=u"最高学历")

    def get_object_display_key(self, datum):
        return 'expertname'

class ExpertsTable(BaseTable):
    mobile = tables.Column('mobile', verbose_name=u"移动电话",
                           policy_rules=[("expertreview", "expertreview:table:column_mobile")])
    workphone = tables.Column('workphone', verbose_name=u"办公电话",
                           policy_rules=[("expertreview", "expertreview:table:column_workphone")])
    yanjiulingyu = tables.Column(get_expert_domains, verbose_name=u"研究领域")
    state = tables.Column(translate_state, verbose_name=u"状态")
    updated_at = tables.Column(calculate_time_since,
                               verbose_name=u"距上次更新",
                               filters=(filters.parse_isotime,
                                        filters.timesince_sortable),
                               attrs={'data-type': 'timesince'})
    class Meta(object):
        name = "expertstable"
        verbose_name = u"专家列表"
        table_actions = (ExpertFilter, ExpertSearch, ExpertCreate,)
        row_actions = (ExpertDetail, ExpertUpdate, ExpertCreateAccount, ExpertSubmit, ExpertCheck, ExpertCheckReject, ExpertDelete, )
        policy_rules = (("expertreview", "expertreview:table:expertstable"),)

