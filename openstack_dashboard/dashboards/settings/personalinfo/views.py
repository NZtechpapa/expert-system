# -*- coding:utf-8 -*-

import logging
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tables
from horizon import version
from horizon import messages
from horizon import workflows

from openstack_dashboard.dashboards.settings.personalinfo import workflows as project_workflows
from openstack_dashboard.dashboards.admin.expertmgmt import workflows as expert_project_workflows
from openstack_dashboard.dashboards.admin.expertmgmt import views as expert_project_views

from openstack_dashboard.utils import expert_db_handle

LOG = logging.getLogger(__name__)

class UpdateView(workflows.WorkflowView):
    template_name = 'settings/personalinfo/update.html'
    workflow_class = project_workflows.UpdateExpertRecord
    page_title = u"修改个人信息"
    policy_rules = (("expertreview", "expertreview:view:expert_update_expert_workflows"),)

    def _check_state(self, expertid):
        expert = expert_db_handle.GetExpertInstanceById(expertid)
        if expert.state != 'draft':
            raise exceptions.NotAuthorized("Illegal Visiting")
        return True

    def get_initial(self):
        initial = super(UpdateView, self).get_initial()
        redirect = reverse("horizon:settings:user:index")
        expertid = expert_db_handle.get_expertid_from_keystone_user(
                       self.request, redirect=redirect)
        self._check_state(expertid)
	expert_project_views.FillContextByexpertid(initial, expertid)
        return initial

class DetailView(UpdateView):
    template_name = 'settings/personalinfo/detail.html'
    workflow_class = project_workflows.DetailExpertRecord
    page_title = u"个人信息"
    policy_rules = (("expertreview", "expertreview:view:expert_view_expert_workflows"),)

    def _check_state(self, expertid):
        expert = expert_db_handle.GetExpertInstanceById(expertid)
        if expert.state == 'waitfor_check':
            self.page_title = u"个人信息（审核中，禁止修改）"
        elif expert.state == 'approved':
            self.page_title = u"个人信息（审核通过）"
        return True
