# -*- coding:utf-8 -*-

import json
import logging
from datetime import date

from horizon import exceptions
from horizon import forms
from horizon import workflows

from django.views.decorators.debug import sensitive_variables
from django.utils import timezone

from openstack_dashboard import models
from openstack_dashboard.utils import project_db_handle
from openstack_dashboard.utils import expert_db_handle

LOG = logging.getLogger(__name__)

# Step 1
_PROJECTBASICINFOFIELDS = ('projectname', 'leibie', 'fuzeren', 'fuzeren_dianhua', 
                           'yewuchushi', 'yewuchushi_dianhua',)
PROJECTBASICINFOFIELDS = ('id', ) + _PROJECTBASICINFOFIELDS

# Step 2
PROJECTREVIEWINFODIELDS = ('shenbaodanwei', 'shenbaoriqi', 'pingshengshijian', 'pingshengdidian', 
                           'chouqurenshu', 'chouquyaoqiu',)

# Step 1
class FillBasicInfoAction(workflows.ModelAction):
    class Meta(object):
        name = u"项目基本信息"
        model = models.Project
        fields = list(_PROJECTBASICINFOFIELDS)

# Step 1
class FillBasicInfo(workflows.Step):
    action_class = FillBasicInfoAction
    contributes = _PROJECTBASICINFOFIELDS
    horizon_description_field = False

# Step 2
class FillReviewInfoAction(workflows.ModelAction):
    def __init__(self, request, *args, **kwargs):
        super(FillReviewInfoAction, self).__init__(request,
                                                   *args,
                                                   **kwargs)
        today = timezone.now().date().isoformat()
        for item in ['shenbaoriqi', 'pingshengshijian']:
            if not item in self.initial or not self.initial[item]:
                self.initial[item] = today

    class Meta(object):
        name = u"项目评审信息"
        model = models.Project
        fields = list(PROJECTREVIEWINFODIELDS)

# Step 2
class FillReviewInfo(workflows.Step):
    action_class = FillReviewInfoAction
    contributes = PROJECTREVIEWINFODIELDS
    horizon_description_field = False

# Entry
class CreateProjectRecord(workflows.Workflow):
    slug = "createproject"
    name = u"录入项目信息"
    finalize_button_name = u"保存"
    success_message = u"项目%s的信息已保存，请确认后提交审核"
    failure_message = u"项目%s的信息保存失败，请检查后台数据库状态"
    success_url = "horizon:admin:projectmgmt:index"
    multipart = True

    default_steps = (FillBasicInfo,
                     FillReviewInfo,
                    )

    @sensitive_variables('context')
    def handle(self, request, context):
        try:
            project_db_handle.CreateProject(**context)
            return True
        except Exception,e:
            exceptions.handle(request)
        return False


# Step 1
class UpdateBasicInfoAction(FillBasicInfoAction):
    id = forms.CharField(label="ID",
                         required=True,
                         widget=forms.HiddenInput())
    class Meta(object):
        name = u"项目基本信息"
        #help_text = u"""项目名支持中英文，最长255字节（中文120字）。"""
        model = models.Project
        fields = list(_PROJECTBASICINFOFIELDS)
# Step 1
class UpdateBasicInfo(workflows.Step):
    action_class = UpdateBasicInfoAction
    contributes = PROJECTBASICINFOFIELDS
    horizon_description_field = False

# Entry
class UpdateProjectRecord(workflows.Workflow):
    slug = "updateproject"
    name = u"修改项目信息"
    finalize_button_name = u"保存"
    success_message = u"项目%s的信息已保存，请确认后提交审核"
    failure_message = u"项目%s的信息保存失败，请检查后台数据库状态"
    success_url = "horizon:admin:projectmgmt:index"
    multipart = True

    default_steps = (UpdateBasicInfo,
                     FillReviewInfo,
                    )

    @sensitive_variables('context')
    def handle(self, request, context):
        try:
            project_db_handle.UpdateProject(**context)
            return True
        except Exception,e:
            exceptions.handle(request)
        return False


# Step 1
class DetailBasicInfoAction(workflows.ReadOnlyModelAction):
    class Meta(object):
        name = u"项目基本信息"
        model = models.Project
        fields = list(_PROJECTBASICINFOFIELDS)

# Step 1
class DetailBasicInfo(workflows.Step):
    action_class = DetailBasicInfoAction
    contributes = _PROJECTBASICINFOFIELDS
    horizon_description_field = False

# Step 2
class DetailReviewInfoAction(workflows.ReadOnlyModelAction):
    class Meta(object):
        name = u"项目评审信息"
        model = models.Project
        fields = list(PROJECTREVIEWINFODIELDS)

# Step 2
class DetailReviewInfo(workflows.Step):
    action_class = DetailReviewInfoAction
    contributes = PROJECTREVIEWINFODIELDS
    horizon_description_field = False

# Entry
class DetailProjectRecord(workflows.Workflow):
    slug = "detailproject"
    name = u"查看项目信息"
    finalize_button_name = ""
    success_url = "horizon:admin:projectmgmt:index"
    multipart = True

    default_steps = (DetailBasicInfo,
                     DetailReviewInfo,
                    )

    def handle(self, request, context):
        return True

