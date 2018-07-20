# -*- coding:utf-8 -*-

import horizon

from openstack_dashboard.dashboards.settings import dashboard

class PersonalInfo(horizon.Panel):
    name = u"个人信息"
    slug = 'personalinfo'
    #policy_rules = (("expertreview", "rule:context_is_uncerti_expert"),)
    policy_rules = (("expertreview", "expertreview:panel:personalinfo"),)
    permissions = (('openstack.roles.uncertified_expert',))

dashboard.Settings.register(PersonalInfo)
