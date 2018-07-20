# -*- coding:utf-8 -*-

import logging
from horizon import exceptions
from horizon import forms
from horizon import workflows
from horizon.utils import validators

from openstack_dashboard.utils import expert_db_handle
from openstack_dashboard.dashboards.admin.expertmgmt import workflows as expert_project_workflows

LOG = logging.getLogger(__name__)

# Entry
class UpdateExpertRecord(expert_project_workflows.UpdateExpertRecord):
    name = u"修改个人信息"
    success_url = "horizon:settings:personalinfo:index"
    default_steps = (expert_project_workflows.FillBasicInfo,
                     expert_project_workflows.FillBankAccountInfo,
                     expert_project_workflows.FillOrganizationInfo,
                     expert_project_workflows.FillHighestEducation,
                     expert_project_workflows.FillOtherInfo,
                     expert_project_workflows.FillAcademicResearchInfo,
                     expert_project_workflows.FillExpertTitleInfo,
                     expert_project_workflows.FillExpertClassInfo,
                     expert_project_workflows.FillExpertDomainInfo,
                     expert_project_workflows.FillExpertFormalJobInfo,
                     expert_project_workflows.FillExpertEducationInfo,
                     expert_project_workflows.FillExpertPartTimeJobInfo,
                     expert_project_workflows.FillExpertReviewHistoryInfo,
                     expert_project_workflows.FillExpertAttachmentInfo,
                    )

    def _clean_data(self, request, context):
        expert_info = super(UpdateExpertRecord, self)._clean_data(request, context)
        expertid = expert_db_handle.get_expertid_from_keystone_user(
            request, redirect=self.success_url)
        expert_info['id'] = expertid
        return expert_info


# Entry
class DetailExpertRecord(workflows.Workflow):
    slug = "detailexpert"
    name = u"查看个人信息"
    finalize_button_name = u"提交审核"
    disable_finalize_button = False
    success_url = "horizon:settings:personalinfo:index"
    multipart = True

    default_steps = (expert_project_workflows.DetailBasicInfo,
                     expert_project_workflows.DetailBankAccountInfo,
                     expert_project_workflows.DetailOrganizationInfo,
                     expert_project_workflows.DetailHighestEducation,
                     expert_project_workflows.DetailOtherInfo,
                     expert_project_workflows.DetailAcademicResearchInfo,
                     expert_project_workflows.DetailExpertTitleInfo,
                     expert_project_workflows.DetailExpertClassInfo,
                     expert_project_workflows.DetailExpertDomainInfo,
                     expert_project_workflows.DetailExpertFormalJobInfo,
                     expert_project_workflows.DetailExpertEducationInfo,
                     expert_project_workflows.DetailExpertPartTimeJobInfo,
                     expert_project_workflows.DetailExpertReviewHistoryInfo,
                     expert_project_workflows.DetailExpertAttachmentInfo,
                    )

    def __init__(self, request=None, context_seed=None, entry_point=None,
                 *args, **kwargs):
        super(DetailExpertRecord, self).__init__(request=request, context_seed=context_seed,
              entry_point=entry_point, *args, **kwargs)
        expertid = expert_db_handle.get_expertid_from_keystone_user(
            request, redirect=self.success_url)
        expert = expert_db_handle.GetExpertInstanceById(expertid)
        if expert and expert.state not in ['draft']:
            self.disable_finalize_button = True

    def handle(self, request, context):
        expertid = expert_db_handle.get_expertid_from_keystone_user(
            request, redirect=self.success_url)
        return expert_db_handle.SubmitExpertInfo(expertid)

