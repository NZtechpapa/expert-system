# -*- coding:utf-8 -*-

import horizon

class Review(horizon.Panel):
    name = u"项目评审"
    slug = 'review'
    policy_rules = (("expertreview", "expertreview:panel:projectreview"),)
    permissions = (('openstack.roles.certified_expert',))

