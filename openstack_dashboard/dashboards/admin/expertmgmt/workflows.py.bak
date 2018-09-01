# -*- coding:utf-8 -*-

from datetime import date
import os
import json
import logging
import six

from horizon import exceptions
from horizon import forms
from horizon import workflows
from horizon.utils import validators

from django.conf import settings
from django.core.files.base import ContentFile  
from django.forms import ValidationError
from django.forms.models import ModelFormMetaclass
from django.forms.models import BaseModelForm
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin.widgets import AdminDateWidget
from django.template.defaultfilters import slugify
from django.views.decorators.debug import sensitive_variables

from openstack_dashboard import models
from openstack_dashboard.utils import expert_db_handle

LOG = logging.getLogger(__name__)

MONTHLIST = {1: u"一月",
             2: u"二月",
             3: u"三月",
             4: u"四月",
             5: u"五月",
             6: u"六月",
             7: u"七月",
             8: u"八月",
             9: u"九月",
             10: u"十月",
             11: u"十一月",
             12: u"十二月"}


UNUSEDFIELDS = ()

YEARLIST = range((date.today().year - 100), (date.today().year + 1))

# Step 1
_USERACCOUNTFIELDS = ('email', 'keystone_username', 'keystone_initial_pwd', )
USERACCOUNTFIELDS = ('id', ) + _USERACCOUNTFIELDS

# Step 2
BASICINFOFIELDS = ('expertname', 'picture', 'cengyong_name', 'pinyin_name', 'gender', 'born',
                   'chushengdi', 'guoji', 'jiguan', 'minzu', 'zhengzhimianmao',
                   'zhengjianleixing', 'zhengjianhaoma',)
# Step 3
BANKACCOUNTFIELDS = ('kaihuyinhang', 'kaihuhuming', 'kaihuzhanghao', 'suoshuzhihang',)
# Step 4
ORGANIZATIONFIELDS = ('suozaidaiwei', 'danweixinzhi', 'suozaibumen', 'danweisuozaisheng',
                      'danweisuozaishi', 'tongxundizhi', 'youzhengbianma', 'zhiwu', 'zhiwujibie',
                      'zhicheng', 'gongzuoxingzhi',)
# Step 5
HIGHESTEDUCATIONFIELDS = ('zuigaoxueli', 'zuigaoxuewei', 'xueweishouyudiqu', 'xueweishouyuriqi',
                          'biyeyuanxiao', 'xueweishouyuyuanxiao', 'suoxuezhuanye', 'xianzhuanye',
                          'isBodao', 'isLiangYuanYuanshi',)
# Step 6
OTHERINFOFIELDS = ('mobile', 'workphone', 'homephone', 'fax', 'personal_web',
                   'weibo', 'jinjilianxiren', 'jinjilianxidianhua', 'zhiyezizhi',)
# Step 7
ACADEMICRESEARCHFIELDS = ('zhuanchangfangxiang', 'gerenjianjie', 'teshujingtie', 'rongyuchenghao',
                          'others',)
# Step 8
_EXPERTTITLEFIELDS = ('rencaichenghao',)
EXPERTTITLEFIELDS = ('rencaichenghaos',)
# Step 9
_EXPERTCLASSFIELDS = ('zhuanjialeixing',)
EXPERTCLASSFIELDS = ('zhuanjialeixings',)
# Step 10
_EXPERTDOMAINFIELDS = ('domainserial', 'domaintype', 'domainname', 'domainkeywords',)
MAX_EXPERTDOMAIN_SLICES = 4
EXPERTDOMAINFIELDS0 = 'expertdomains'
EXPERTDOMAINFIELDS1 = expert_db_handle.generate_slices_fields(_EXPERTDOMAINFIELDS,
                                                              MAX_EXPERTDOMAIN_SLICES)
EXPERTDOMAINFIELDS = (EXPERTDOMAINFIELDS0,) + EXPERTDOMAINFIELDS1
UNUSEDFIELDS = UNUSEDFIELDS + EXPERTDOMAINFIELDS1
# Step 11
_EXPERTFORMALJOBFIELDS = ('formaljob_serial', 'formaljob_start', 'formaljob_end',
                          'formaljob_country', 'formaljob_danwei', 'formaljob_zhiwu',
                          'formaljob_zhiwujibie', 'formaljob_zhichen', 'formaljob_yanjiufangxiang',
                          'formaljob_gongzuoneirong', 'formaljob_gongzuoxingzhi')
MAX_EXPERTFORMALJOB_SLICES = 8
EXPERTFORMALJOBFIELDS0 = 'formaljobs'
EXPERTFORMALJOBFIELDS1 = expert_db_handle.generate_slices_fields(_EXPERTFORMALJOBFIELDS,
                                                                 MAX_EXPERTFORMALJOB_SLICES)
EXPERTFORMALJOBFIELDS = (EXPERTFORMALJOBFIELDS0,) + EXPERTFORMALJOBFIELDS1
UNUSEDFIELDS = UNUSEDFIELDS + EXPERTFORMALJOBFIELDS1

# Step 12
_EXPERTEDUCATIONFIELDS = ('education_serial', 'education_start', 'education_end',
                          'education_country', 'education_yuanxiaomingcheng', 'education_zhuanye',
                          'education_xueli', 'education_xuewei', 'education_peixunjinxiu',
                          'education_zhidaojiaoshi',)
MAX_EXPERTEDUCATION_SLICES = 6
EXPERTEDUCATIONFIELDS0 = 'educations'
EXPERTEDUCATIONFIELDS1 = expert_db_handle.generate_slices_fields(_EXPERTEDUCATIONFIELDS,
                                                                 MAX_EXPERTEDUCATION_SLICES)
EXPERTEDUCATIONFIELDS = (EXPERTEDUCATIONFIELDS0,) + EXPERTEDUCATIONFIELDS1
UNUSEDFIELDS = UNUSEDFIELDS + EXPERTEDUCATIONFIELDS1

# Step 13
_EXPERTPARTTIMEJOBFIELDS = ('parttimejob_serial', 'parttimejob_start', 'parttimejob_end',
                            'parttimejob_danwei', 'parttimejob_zhiwu', 'parttimejob_sessionid',)
MAX_EXPERTPARTTIMEJOB_SLICES = 10
EXPERTPARTTIMEJOBFIELDS0 = 'parttimejobs'
EXPERTPARTTIMEJOBFIELDS1 = expert_db_handle.generate_slices_fields(_EXPERTPARTTIMEJOBFIELDS,
                                                                   MAX_EXPERTPARTTIMEJOB_SLICES)
EXPERTPARTTIMEJOBFIELDS = (EXPERTPARTTIMEJOBFIELDS0,) + EXPERTPARTTIMEJOBFIELDS1
UNUSEDFIELDS = UNUSEDFIELDS + EXPERTPARTTIMEJOBFIELDS1

# Step 14
_EXPERTREVIEWHISTORYFIELDS = ('reviewhistory_serial', 'reviewhistory_start', 'reviewhistory_end',
                              'reviewhistory_content', 'reviewhistory_weituojigou',)
MAX_EXPERTREVIEWHISTORY_SLICES = 20
EXPERTREVIEWHISTORYFIELDS0 = 'reviewhistories'
EXPERTREVIEWHISTORYFIELDS1 = expert_db_handle.generate_slices_fields(_EXPERTREVIEWHISTORYFIELDS,
                                                                     MAX_EXPERTREVIEWHISTORY_SLICES)
EXPERTREVIEWHISTORYFIELDS = (EXPERTREVIEWHISTORYFIELDS0,) + EXPERTREVIEWHISTORYFIELDS1
UNUSEDFIELDS = UNUSEDFIELDS + EXPERTREVIEWHISTORYFIELDS1

# Step 15
_EXPERTXIANGMUINFOFIELDS = ('xiangmuinfo_serial', 'xiangmuinfo_name', 'xiangmuinfo_jibie',
                            'xiangmuinfo_paiming', 'xiangmuinfo_bianhao', 'xiangmuinfo_zizhuleibie',
                            'xiangmuinfo_jingfei', 'xiangmuinfo_start', 'xiangmuinfo_end',)
MAX_EXPERTXIANGMUINFO_SLICES = 10
EXPERTXIANGMUINFOFIELDS0 = 'xiangmuinfos'
EXPERTXIANGMUINFOFIELDS1 = expert_db_handle.generate_slices_fields(_EXPERTXIANGMUINFOFIELDS,
                                                                   MAX_EXPERTXIANGMUINFO_SLICES)
EXPERTXIANGMUINFOFIELDS = (EXPERTXIANGMUINFOFIELDS0,) + EXPERTXIANGMUINFOFIELDS1
UNUSEDFIELDS = UNUSEDFIELDS + EXPERTXIANGMUINFOFIELDS1

# Step 16
_EXPERTATTACHMENTFIELDS = ('attachment_serial', 'attachment_name', 'attachment_type',
                           'attachment_file',)
MAX_EXPERTATTACHMENT_SLICES = 8
EXPERTATTACHMENTFIELDS0 = 'attachments'
EXPERTATTACHMENTFIELDS1 = expert_db_handle.generate_slices_fields(_EXPERTATTACHMENTFIELDS,
                                                                  MAX_EXPERTATTACHMENT_SLICES)
EXPERTATTACHMENTFIELDS = (EXPERTATTACHMENTFIELDS0,) + EXPERTATTACHMENTFIELDS1
UNUSEDFIELDS = UNUSEDFIELDS + EXPERTATTACHMENTFIELDS1

class NoVerifyContributes(object):
    def _verify_contributions(self, context):
        return True

#============================================================
#== Create                                                  =
#============================================================
# Step 1
class FillUserAccountInfoAction(workflows.ModelAction):
    confirm_password = forms.CharField(
        label=u"确认密码",
        widget=forms.PasswordInput(render_value=False))

    no_autocomplete = True

    def _clean__keystone_username(self, data):
        if 'keystone_username' in data:
            keystone_username = data['keystone_username']
            if expert_db_handle.GetExpertInstanceByKeystoneUsername(keystone_username):
                raise ValidationError(u"该账户%s已存在" % keystone_username)

    def clean(self):
        '''Check to make sure password fields match.'''
        data = super(FillUserAccountInfoAction, self).clean()
        if 'keystone_initial_pwd' in data and 'confirm_password' in data:
            if data['keystone_initial_pwd'] != data['confirm_password']:
                raise ValidationError(u"两次输入密码不一致")
            if not data['keystone_initial_pwd']:
                del data['keystone_initial_pwd']
        self._clean__keystone_username(data)
        return data

    def __init__(self, request, *args, **kwargs):
        super(FillUserAccountInfoAction, self).__init__(request,
                                                        *args,
                                                        **kwargs)
        self.fields["keystone_initial_pwd"].widget = forms.PasswordInput(render_value=False)
        self.fields["keystone_initial_pwd"].regex = validators.password_validator()

    class Meta(object):
        name = u"账号信息"
        slug = u"filluseraccountinfoaction"
        help_text = u"""该页信息用于创建专家账号
电子邮箱用于找回密码
所有信息均为创建专家账号所必填信息"""
        model = models.Expert
        fields = list(USERACCOUNTFIELDS)

# Step 1
class FillUserAccountInfo(workflows.Step):
    action_class = FillUserAccountInfoAction
    contributes = USERACCOUNTFIELDS

# Step 2
class FillBasicInfoAction(workflows.ModelAction):
    def __init__(self, request, *args, **kwargs):
        super(FillBasicInfoAction, self).__init__(request,
                                                  *args,
                                                  **kwargs)
        if not self.initial.get('born', ''):
            self.fields["born"].initial = date(date.today().year - 40, 1, 1)
    def clean(self):
        data = super(FillBasicInfoAction, self).clean()
        if data['zhengjianleixing'] == u"身份证":
            if not validators.validate_CHN_id_no(data['zhengjianhaoma']):
                raise ValidationError(u"身份证号格式不正确。请填写15位或18位身份证号")
        return data

    def get_help_text(self, extra_context=None):
        extra = {} if extra_context is None else dict(extra_context)
        pic = self.initial.get('picture', '')
        if pic:
            extra['uploaded_picture'] = settings.MEDIA_URL + pic
        extra['show_help_text'] = True
        return super(FillBasicInfoAction, self).get_help_text(extra)

    class Meta(object):
        name = u"基本信息"
        slug = u"fillbasicinfoaction"
        help_text_template = "admin/expertmgmt/_basic_info_help.html"
        model = models.Expert
        fields = list(BASICINFOFIELDS)

# Step 2
class FillBasicInfo(workflows.Step):
    action_class = FillBasicInfoAction
    contributes = BASICINFOFIELDS

# Step 3
class FillBankAccountInfoAction(workflows.ModelAction):
    class Meta(object):
        name = u"银行账号信息"
        slug = u"fillbankaccountinfoaction"
        help_text = u"""仅用于评审费用转账"""
        model = models.Expert
        fields = list(BANKACCOUNTFIELDS)

# Step 3
class FillBankAccountInfo(workflows.Step):
    action_class = FillBankAccountInfoAction
    contributes = BANKACCOUNTFIELDS

# Step 4
class FillOrganizationInfoAction(workflows.ModelAction):
    class Meta(object):
        name = u"所在单位信息"
        slug = u"fillorganizationinfoaction"
        help_text = u"""填写目前就职单位信息"""
        model = models.Expert
        fields = list(ORGANIZATIONFIELDS)

# Step 4
class FillOrganizationInfo(workflows.Step):
    action_class = FillOrganizationInfoAction
    contributes = ORGANIZATIONFIELDS

# Step 5
class FillHighestEducationAction(workflows.ModelAction):
    class Meta(object):
        name = u"最高学历学位信息"
        slug = u"fillhighesteducationaction"
        help_text = u"""填写最高学历学位信息"""
        model = models.Expert
        fields = list(HIGHESTEDUCATIONFIELDS)

# Step 5
class FillHighestEducation(workflows.Step):
    action_class = FillHighestEducationAction
    contributes = HIGHESTEDUCATIONFIELDS

# Step 6
class FillOtherInfoAction(workflows.ModelAction):
    def __init__(self, request, *args, **kwargs):
        super(FillOtherInfoAction, self).__init__(request,
                                                  *args,
                                                  **kwargs)
        self.fields["mobile"].regex = validators.phone_validator()
        self.fields["workphone"].regex = validators.phone_validator()
        self.fields["homephone"].regex = validators.phone_validator()
        self.fields["fax"].regex = validators.phone_validator()
        self.fields["jinjilianxidianhua"].regex = validators.phone_validator()
        all_roles = [ d.get('name') for d in request.user.roles ]
        for r in ['yewuchu', 'fenguanjuzhang', 'juzhang']:
            if r in all_roles:
                self.fields["mobile"].widget = forms.HiddenInput()
                self.fields["workphone"].widget = forms.HiddenInput()
                break

    class Meta(object):
        name = u"其他信息"
        slug = u"fillotherinfoaction"
        help_text = u"""填写手机号码及座机号码等其他信息"""
        model = models.Expert
        fields = list(OTHERINFOFIELDS)

# Step 6
class FillOtherInfo(workflows.Step):
    action_class = FillOtherInfoAction
    contributes = OTHERINFOFIELDS

# Step 7
class FillAcademicResearchInfoAction(workflows.ModelAction):
    class Meta(object):
        name = u"学术专长或研究方向"
        slug = u"fillacademicresearchinfoaction"
        help_text = u"""填写学术专长或研究方向"""
        model = models.Expert
        fields = list(ACADEMICRESEARCHFIELDS)

# Step 7
class FillAcademicResearchInfo(workflows.Step):
    action_class = FillAcademicResearchInfoAction
    contributes = ACADEMICRESEARCHFIELDS

# Step 8
class FillExpertTitleInfoAction(workflows.ModelAction):
    rencaichenghaos = forms.MultipleChoiceField(
        required=False,
        initial=u"无",
        widget=forms.CheckboxSelectMultiple())

    def __init__(self, request, *args, **kwargs):
        super(FillExpertTitleInfoAction, self).__init__(request,
                                                        *args,
                                                        **kwargs)
        src = self.fields["rencaichenghao"]
        dst = self.fields["rencaichenghaos"]
        src.widget = forms.HiddenInput()
        dst.choices = list(src.choices)[1:]
        dst.label = src.label
        dst.help_text = src.help_text

    class Meta(object):
        name = u"人才称号"
        slug = u"fillexperttitleinfoaction"
        help_text = u"""填写学术专长或研究方向"""
        model = models.ExpertTitle
        fields = list(_EXPERTTITLEFIELDS)

# Step 8
class FillExpertTitleInfo(workflows.Step):
    action_class = FillExpertTitleInfoAction
    contributes = EXPERTTITLEFIELDS

# Step 9
class FillExpertClassInfoAction(workflows.ModelAction):
    zhuanjialeixings = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple())

    def __init__(self, request, *args, **kwargs):
        super(FillExpertClassInfoAction, self).__init__(request,
                                                        *args,
                                                        **kwargs)
        src = self.fields["zhuanjialeixing"]
        dst = self.fields["zhuanjialeixings"]
        src.widget = forms.HiddenInput()
        dst.choices = list(src.choices)[1:]
        dst.label = src.label
        dst.help_text = src.help_text

    class Meta(object):
        name = u"专家类型"
        slug = u"fillexpertclassinfoaction"
        help_text = u"""选择所属类型（可多选）"""
        model = models.ExpertClass
        fields = list(_EXPERTCLASSFIELDS)

# Step 9
class FillExpertClassInfo(workflows.Step):
    action_class = FillExpertClassInfoAction
    contributes = EXPERTCLASSFIELDS

# Step 10
class FillExpertDomainInfoAction(workflows.ModelAction):
    def __init__(self, request, *args, **kwargs):
        super(FillExpertDomainInfoAction, self).__init__(request,
                                                         *args,
                                                         **kwargs)
        readonlyInput = forms.TextInput(attrs={'readonly': 'readonly'})
        self._initial_serial_field('domainserial')
        _src = 'domaintype'
        for i in range(1, 1 + self.maxslices):
            _dst = '%s%d' % (_src, i)
            dst = self.fields[_dst]
            if not dst.initial:
                _i = i if i < len(dst.choices) else (len(dst.choices) - 1)
                (initial, _value) = dst.choices[_i]
                dst.initial = initial

    class Meta(object):
        name = u"研究领域"
        slug = u"fillexpertdomaininfoaction"
        help_text = u"""填写在各个领域中所研究的学科名称以及中文关键词"""
        model = models.ExpertDomain
        fields = list(_EXPERTDOMAINFIELDS)
        output = EXPERTDOMAINFIELDS0
        maxslices = MAX_EXPERTDOMAIN_SLICES

# Step 10
class FillExpertDomainInfo(NoVerifyContributes, workflows.Step):
    action_class = FillExpertDomainInfoAction
    contributes = EXPERTDOMAINFIELDS
    template_name = "admin/expertmgmt/_create_expertdomaininfo.html"

# Step 11
class FillExpertFormalJobInfoAction(workflows.ModelAction):
    def __init__(self, request, *args, **kwargs):
        super(FillExpertFormalJobInfoAction, self).__init__(request,
                                                            *args,
                                                            **kwargs)
        self._initial_serial_field('formaljob_serial')

    class Meta(object):
        name = u"工作履历"
        slug = u"fillexpertformaljobinfoaction"
        help_text = u"""填写工作履历"""
        plus_action_name = u"+ 添加工作经历"
        model = models.FormalJob
        fields = list(_EXPERTFORMALJOBFIELDS)
        table_format = [
            ['formaljob_serial'],
            ['formaljob_start', 'formaljob_end'],
            ['formaljob_country', 'formaljob_danwei'],
            ['formaljob_zhiwu', 'formaljob_zhiwujibie'],
            ['formaljob_zhichen'],
            ['formaljob_yanjiufangxiang', 'formaljob_gongzuoxingzhi'],
            ['formaljob_gongzuoneirong'],
        ]
        output = EXPERTFORMALJOBFIELDS0
        maxslices = MAX_EXPERTFORMALJOB_SLICES

# Step 11
class FillExpertFormalJobInfo(NoVerifyContributes, workflows.Step):
    action_class = FillExpertFormalJobInfoAction
    contributes = EXPERTFORMALJOBFIELDS
    template_name = "admin/expertmgmt/_create_step_multi_table_form.html"

# Step 12
class FillExpertEducationInfoAction(workflows.ModelAction):
    def __init__(self, request, *args, **kwargs):
        super(FillExpertEducationInfoAction, self).__init__(request,
                                                              *args,
                                                              **kwargs)
        self._initial_serial_field('education_serial')

    class Meta(object):
        name = u"教育信息"
        slug = u"fillexperteducationinfoaction"
        help_text = u"""填写接受教育信息"""
        plus_action_name = u"+ 添加教育经历"
        model = models.Education
        fields = list(_EXPERTEDUCATIONFIELDS)
        table_format = [
            ['education_serial'],
            ['education_start', 'education_end'],
            ['education_country', 'education_yuanxiaomingcheng'],
            ['education_zhuanye'],
            ['education_xueli', 'education_xuewei'],
            ['education_peixunjinxiu'],
            ['education_zhidaojiaoshi'],
        ]
        output = EXPERTEDUCATIONFIELDS0
        maxslices = MAX_EXPERTEDUCATION_SLICES

# Step 12
class FillExpertEducationInfo(NoVerifyContributes, workflows.Step):
    action_class = FillExpertEducationInfoAction
    contributes = EXPERTEDUCATIONFIELDS
    template_name = "admin/expertmgmt/_create_step_multi_table_form.html"

# Step 13
class FillExpertPartTimeJobInfoAction(workflows.ModelAction):
    def __init__(self, request, *args, **kwargs):
        super(FillExpertPartTimeJobInfoAction, self).__init__(request,
                                                              *args,
                                                              **kwargs)
        self._initial_serial_field('parttimejob_serial')

    class Meta(object):
        name = u"学术兼职"
        slug = u"fillexpertparttimejobinfoaction"
        help_text = u"""填写学术兼职信息"""
        plus_action_name = u"+ 添加学术兼职经历"
        model = models.PartTimeJob
        fields = list(_EXPERTPARTTIMEJOBFIELDS)
        table_format = [
            ['parttimejob_serial', 'parttimejob_sessionid'],
            ['parttimejob_start', 'parttimejob_end'],
            ['parttimejob_danwei', 'parttimejob_zhiwu'],
        ]
        output = EXPERTPARTTIMEJOBFIELDS0
        maxslices = MAX_EXPERTPARTTIMEJOB_SLICES

# Step 13
class FillExpertPartTimeJobInfo(NoVerifyContributes, workflows.Step):
    action_class = FillExpertPartTimeJobInfoAction
    contributes = EXPERTPARTTIMEJOBFIELDS
    template_name = "admin/expertmgmt/_create_step_multi_table_form.html"

# Step 14
class FillExpertReviewHistoryInfoAction(workflows.ModelAction):
    def __init__(self, request, *args, **kwargs):
        super(FillExpertReviewHistoryInfoAction, self).__init__(request,
                                                                *args,
                                                                **kwargs)
        self._initial_serial_field('reviewhistory_serial')

    class Meta(object):
        name = u"学术评审"
        slug = u"fillexpertreviewhistoryinfoaction"
        help_text = u"""填写学术评审信息"""
        plus_action_name = u"+ 添加学术评审信息"
        model = models.ReviewHistory
        fields = list(_EXPERTREVIEWHISTORYFIELDS)
        table_format = [
            ['reviewhistory_serial'],
            ['reviewhistory_start', 'reviewhistory_end'],
            ['reviewhistory_weituojigou'],
            ['reviewhistory_content'],
        ]
        output = EXPERTREVIEWHISTORYFIELDS0
        maxslices = MAX_EXPERTREVIEWHISTORY_SLICES

# Step 14
class FillExpertReviewHistoryInfo(NoVerifyContributes, workflows.Step):
    action_class = FillExpertReviewHistoryInfoAction
    contributes = EXPERTREVIEWHISTORYFIELDS
    template_name = "admin/expertmgmt/_create_step_multi_table_form.html"

# Step 15
class FillExpertXiangmuInfoAction(workflows.ModelAction):
    def __init__(self, request, *args, **kwargs):
        super(FillExpertXiangmuInfoAction, self).__init__(request,
                                                           *args,
                                                           **kwargs)
        self._initial_serial_field('xiangmuinfo_serial')
    class Meta(object):
        name = u"承担项目情况"
        slug = u"fillexpertxiangmuinfoaction"
        help_text = u"""填写所承担过的项目信息"""
        plus_action_name = u"+ 添加项目信息"
        model = models.XiangmuInfo
        fields = list(_EXPERTXIANGMUINFOFIELDS)
        table_format = [
            ['xiangmuinfo_serial'],
            ['xiangmuinfo_start', 'xiangmuinfo_end'],
            ['xiangmuinfo_name', 'xiangmuinfo_jibie'],
            ['xiangmuinfo_paiming', 'xiangmuinfo_bianhao'],
            ['xiangmuinfo_zizhuleibie', 'xiangmuinfo_jingfei'],
        ]
        output = EXPERTXIANGMUINFOFIELDS0
        maxslices = MAX_EXPERTXIANGMUINFO_SLICES

# Step 15
class FillExpertXiangmuInfo(NoVerifyContributes, workflows.Step):
    action_class = FillExpertXiangmuInfoAction
    contributes = EXPERTXIANGMUINFOFIELDS
    template_name = "admin/expertmgmt/_create_step_multi_table_form.html"

# Step 16
class FillExpertAttachmentInfoAction(workflows.ModelAction):
    def __init__(self, request, *args, **kwargs):
        super(FillExpertAttachmentInfoAction, self).__init__(request,
                                                             *args,
                                                             **kwargs)
        self._initial_serial_field('attachment_serial')

    def clean(self):
        data = super(FillExpertAttachmentInfoAction, self).clean()
        for f in data['attachments']:
            i = f['attachment_serial']
            _attachment_file = self.request.FILES.get('attachment_file%d' % i, None)
            if _attachment_file:
                f['attachment_file'] = _attachment_file
                if not f['attachment_name']:
                    f['attachment_name'] = _attachment_file.name
        return data

    def get_help_text(self, extra_context=None):
        extra = {} if extra_context is None else dict(extra_context)
        attachments = []
        for i in range(1, 1 + self.maxslices):
            _fpath = 'attachment_file%d' % i
            _fname = 'attachment_name%d' % i
            _ftype = 'attachment_type%d' % i
            _fid = 'attachment_serial%d' % i
            fpath = self.initial.get(_fpath, '')
            fname = self.initial.get(_fname, '')
            ftype = self.initial.get(_ftype, '')
            fid = self.initial.get(_fid , '')
            if not (fpath and fname and ftype and fid):
                continue
            attachment = {}
            attachment['attachment_file'] = settings.MEDIA_URL + fpath
            attachment['attachment_name'] = fname
            attachment['attachment_type'] = ftype
            attachment['attachment_serial'] = fid
            attachments.append(attachment)

        extra['attachments'] = attachments
        extra['show_help_text'] = True
        return super(FillExpertAttachmentInfoAction, self).get_help_text(extra)

    class Meta(object):
        name = u"附件"
        slug = u"fillexpertattachmentinfoaction"
        help_text_template = "admin/expertmgmt/_attachment_help.html"
        plus_action_name = u"+ 添加附件"
        model = models.Attachment
        fields = list(_EXPERTATTACHMENTFIELDS)
        table_format = [
            ['attachment_serial'],
            ['attachment_name', 'attachment_type'],
            ['attachment_file'],
        ]
        output = EXPERTATTACHMENTFIELDS0
        maxslices = MAX_EXPERTATTACHMENT_SLICES

# Step 16
class FillExpertAttachmentInfo(NoVerifyContributes, workflows.Step):
    action_class = FillExpertAttachmentInfoAction
    contributes = EXPERTATTACHMENTFIELDS
    template_name = "admin/expertmgmt/_create_step_multi_table_form.html"


# Entry
class CreateExpertRecord(workflows.Workflow):
    slug = "createexpert"
    name = u"录入专家信息"
    finalize_button_name = u"保存"
    success_message = u"专家%s的信息已保存，请确认后提交审核"
    failure_message = u"专家%s的信息保存失败，请检查后台数据库状态"
    success_url = "horizon:admin:expertmgmt:index"
    multipart = True

    default_steps = (FillUserAccountInfo,
                     FillBasicInfo,
                     FillBankAccountInfo,
                     FillOrganizationInfo,
                     FillHighestEducation,
                     FillOtherInfo,
                     FillAcademicResearchInfo,
                     FillExpertTitleInfo,
                     FillExpertClassInfo,
                     FillExpertDomainInfo,
                     FillExpertFormalJobInfo,
                     FillExpertEducationInfo,
                     FillExpertPartTimeJobInfo,
                     FillExpertReviewHistoryInfo,
                     FillExpertXiangmuInfo,
                     FillExpertAttachmentInfo,
                    )

    @sensitive_variables('context')
    def handle(self, request, context):
        expert_info = {}
        for i in context:
            if i not in UNUSEDFIELDS:
                expert_info[i] = context[i]
        expert_info['picture'] = request.FILES.get('picture', None)
        #for f in expert_info['attachments']:
        #    i = f['attachment_serial']
        #    f['attachment_file'] = request.FILES.get('attachment_file%d' % i, None)
        try:
            expert_db_handle.CreateExpert(**expert_info)
            return True
        except Exception,e:
            exceptions.handle(request)
        return False

#============================================================
#== Edit information                                        =
#============================================================
# Step 1
class UpdateUserAccountInfoAction(FillUserAccountInfoAction):
    id = forms.CharField(label="ID",
                         required=True,
                         widget=forms.HiddenInput())

    # Don't check keystone username as it's not allowed to be updated
    def _clean__keystone_username(self, data):
        return

    def __init__(self, request, *args, **kwargs):
        super(UpdateUserAccountInfoAction, self).__init__(request,
                                                          *args,
                                                          **kwargs)
        readonlyInput = forms.TextInput(attrs={'readonly': 'readonly'})
        self.fields["email"].widget = readonlyInput
        self.fields["keystone_username"].widget = readonlyInput
        self.fields["keystone_initial_pwd"].required = False
        self.fields["confirm_password"].required = False

    class Meta(object):
        name = u"账号信息"
        slug = u"updateuseraccountinfoaction"
        help_text = u"""该页信息用于创建专家账号
电子邮箱用于找回密码
所有信息均为创建专家账号所必填信息"""
        model = models.Expert
        fields = list(_USERACCOUNTFIELDS)

# Step 1
class UpdateUserAccountInfo(workflows.Step):
    action_class = UpdateUserAccountInfoAction
    contributes = USERACCOUNTFIELDS

# Entry
class UpdateExpertRecord(workflows.Workflow):
    slug = "updateexpert"
    name = u"修改专家信息"
    finalize_button_name = u"保存"
    success_message = u"专家%s的信息已保存，请确认后提交审核"
    failure_message = u"专家%s的信息保存失败，请检查后台数据库状态"
    success_url = "horizon:admin:expertmgmt:index"
    multipart = True

    default_steps = (UpdateUserAccountInfo,
                     FillBasicInfo,
                     FillBankAccountInfo,
                     FillOrganizationInfo,
                     FillHighestEducation,
                     FillOtherInfo,
                     FillAcademicResearchInfo,
                     FillExpertTitleInfo,
                     FillExpertClassInfo,
                     FillExpertDomainInfo,
                     FillExpertFormalJobInfo,
                     FillExpertEducationInfo,
                     FillExpertPartTimeJobInfo,
                     FillExpertReviewHistoryInfo,
                     FillExpertXiangmuInfo,
                     FillExpertAttachmentInfo,
                    )

    def _clean_data(self, request, context):
        expert_info = {}
        for i in context:
            if i not in UNUSEDFIELDS:
                expert_info[i] = context[i]
        if request.FILES.get('picture', None):
            expert_info['picture'] = request.FILES['picture']

        return expert_info

    @sensitive_variables('context')
    def handle(self, request, context):
        expert_info = self._clean_data(request, context)
        try:
            expert_db_handle.UpdateExpert(**expert_info)
            return True
        except Exception,e:
            exceptions.handle(request)
        return False


#============================================================
#== Detail information Show                                 =
#============================================================
# Step 1
class DetailUserAccountInfoAction(workflows.ReadOnlyModelAction):
    def __init__(self, request, *args, **kwargs):
        super(DetailUserAccountInfoAction, self).__init__(request,
                                                          *args,
                                                          **kwargs)
        all_roles = [ d.get('name') for d in request.user.roles ]
        for r in ['xinxichu', 'yewuchu', 'fenguanjuzhang', 'juzhang']:
            if r in all_roles:
                self.fields["keystone_initial_pwd"].widget = forms.HiddenInput()
                break

    class Meta(object):
        name = u"账号信息"
        slug = u"detailuseraccountinfoaction"
        model = models.Expert
        fields = list(USERACCOUNTFIELDS)

# Step 1
class DetailUserAccountInfo(workflows.Step):
    action_class = DetailUserAccountInfoAction
    contributes = USERACCOUNTFIELDS
    horizon_description_field = True

# Step 2
class DetailBasicInfoAction(workflows.ReadOnlyModelAction):
    def __init__(self, request, *args, **kwargs):
        super(DetailBasicInfoAction, self).__init__(request, *args, **kwargs)
        self.fields['picture'].widget = forms.HiddenInput()

    def get_help_text(self, extra_context=None):
        extra = {} if extra_context is None else dict(extra_context)
        pic = self.initial.get('picture', '')
        if pic:
            extra['uploaded_picture'] = settings.MEDIA_URL + pic
        extra['show_help_text'] = False
        return super(DetailBasicInfoAction, self).get_help_text(extra)

    class Meta(object):
        name = u"基本信息"
        slug = u"detailbasicinfoaction"
        help_text_template = "admin/expertmgmt/_basic_info_help.html"
        model = models.Expert
        fields = list(BASICINFOFIELDS)

# Step 2
class DetailBasicInfo(workflows.Step):
    action_class = DetailBasicInfoAction
    contributes = BASICINFOFIELDS
    horizon_description_field = True

# Step 3
class DetailBankAccountInfoAction(workflows.ReadOnlyModelAction):
    class Meta(object):
        name = u"银行账号信息"
        slug = u"detailbankaccountinfoaction"
        model = models.Expert
        fields = list(BANKACCOUNTFIELDS)

# Step 3
class DetailBankAccountInfo(workflows.Step):
    action_class = DetailBankAccountInfoAction
    contributes = BANKACCOUNTFIELDS
    horizon_description_field = True

# Step 4
class DetailOrganizationInfoAction(workflows.ReadOnlyModelAction):
    class Meta(object):
        name = u"所在单位信息"
        slug = u"detailorganizationinfoaction"
        model = models.Expert
        fields = list(ORGANIZATIONFIELDS)

# Step 4
class DetailOrganizationInfo(workflows.Step):
    action_class = DetailOrganizationInfoAction
    contributes = ORGANIZATIONFIELDS
    horizon_description_field = True

# Step 5
class DetailHighestEducationAction(workflows.ReadOnlyModelAction):
    class Meta(object):
        name = u"最高学历学位信息"
        slug = u"detailhighesteducationaction"
        model = models.Expert
        fields = list(HIGHESTEDUCATIONFIELDS)

# Step 5
class DetailHighestEducation(workflows.Step):
    action_class = DetailHighestEducationAction
    contributes = HIGHESTEDUCATIONFIELDS
    horizon_description_field = True

# Step 6
class DetailOtherInfoAction(workflows.ReadOnlyModelAction):
    def __init__(self, request, *args, **kwargs):
        super(DetailOtherInfoAction, self).__init__(request,
                                                    *args,
                                                    **kwargs)
        all_roles = [ d.get('name') for d in request.user.roles ]
        for r in ['yewuchu', 'fenguanjuzhang', 'juzhang']:
            if r in all_roles:
                self.fields["mobile"].widget = forms.HiddenInput()
                self.fields["workphone"].widget = forms.HiddenInput()
                break
        
    class Meta(object):
        name = u"其他信息"
        slug = u"detailotherinfoaction"
        model = models.Expert
        fields = list(OTHERINFOFIELDS)

# Step 6
class DetailOtherInfo(workflows.Step):
    action_class = DetailOtherInfoAction
    contributes = OTHERINFOFIELDS
    horizon_description_field = True

# Step 7
class DetailAcademicResearchInfoAction(workflows.ReadOnlyModelAction):
    class Meta(object):
        name = u"个人简历以及学术专长或研究方向"
        slug = u"detailacademicresearchinfoaction"
        model = models.Expert
        fields = list(ACADEMICRESEARCHFIELDS)

# Step 7
class DetailAcademicResearchInfo(workflows.Step):
    action_class = DetailAcademicResearchInfoAction
    contributes = ACADEMICRESEARCHFIELDS
    horizon_description_field = True

# Step 8
class DetailExpertTitleInfoAction(workflows.ReadOnlyModelAction):
    rencaichenghaos = forms.MultipleChoiceField(
        required=False,
        initial=u"无",
        disabled=True,
        widget=forms.CheckboxSelectMultiple())

    def __init__(self, request, *args, **kwargs):
        super(DetailExpertTitleInfoAction, self).__init__(request,
                                                          *args,
                                                          **kwargs)
        src = self.fields["rencaichenghao"]
        dst = self.fields["rencaichenghaos"]
        src.widget = forms.HiddenInput()
        dst.choices = list(src.choices)[1:]
        dst.label = src.label
        dst.help_text = src.help_text

    class Meta(object):
        name = u"人才称号"
        slug = u"detailexperttitleinfoaction"
        model = models.ExpertTitle
        fields = list(_EXPERTTITLEFIELDS)

# Step 8
class DetailExpertTitleInfo(workflows.Step):
    action_class = DetailExpertTitleInfoAction
    contributes = EXPERTTITLEFIELDS
    horizon_description_field = True

# Step 9
class DetailExpertClassInfoAction(workflows.ReadOnlyModelAction):
    zhuanjialeixings = forms.MultipleChoiceField(
        required=False,
        disabled=True,
        widget=forms.CheckboxSelectMultiple())

    def __init__(self, request, *args, **kwargs):
        super(DetailExpertClassInfoAction, self).__init__(request,
                                                          *args,
                                                          **kwargs)
        src = self.fields["zhuanjialeixing"]
        dst = self.fields["zhuanjialeixings"]
        src.widget = forms.HiddenInput()
        dst.choices = list(src.choices)[1:]
        dst.label = src.label
        dst.help_text = src.help_text

    class Meta(object):
        name = u"专家类型"
        slug = u"detailexpertclassinfoaction"
        model = models.ExpertClass
        fields = list(_EXPERTCLASSFIELDS)

# Step 9
class DetailExpertClassInfo(workflows.Step):
    action_class = DetailExpertClassInfoAction
    contributes = EXPERTCLASSFIELDS
    horizon_description_field = True

# Step 10
class DetailExpertDomainInfoAction(workflows.ReadOnlyModelAction):
    class Meta(object):
        name = u"研究领域"
        slug = u"detailexpertdomaininfoaction"
        model = models.ExpertDomain
        fields = list(_EXPERTDOMAINFIELDS)
        maxslices = MAX_EXPERTDOMAIN_SLICES

# Step 10
class DetailExpertDomainInfo(NoVerifyContributes, workflows.Step):
    action_class = DetailExpertDomainInfoAction
    contributes = EXPERTDOMAINFIELDS
    template_name = "admin/expertmgmt/_create_expertdomaininfo.html"

# Step 11
class DetailExpertFormalJobInfoAction(workflows.ReadOnlyModelAction):
    class Meta(object):
        name = u"工作履历"
        slug = u"detailexpertformaljobinfoaction"
        plus_action_name = u"+ 添加工作经历"
        model = models.FormalJob
        fields = list(_EXPERTFORMALJOBFIELDS)
        table_format = [
            ['formaljob_serial'],
            ['formaljob_start', 'formaljob_end'],
            ['formaljob_country', 'formaljob_danwei'],
            ['formaljob_zhiwu', 'formaljob_zhiwujibie'],
            ['formaljob_zhichen'],
            ['formaljob_yanjiufangxiang', 'formaljob_gongzuoxingzhi'],
            ['formaljob_gongzuoneirong'],
        ]
        output = EXPERTFORMALJOBFIELDS0
        maxslices = MAX_EXPERTFORMALJOB_SLICES

# Step 11
class DetailExpertFormalJobInfo(NoVerifyContributes, workflows.Step):
    action_class = DetailExpertFormalJobInfoAction
    contributes = EXPERTFORMALJOBFIELDS
    template_name = "admin/expertmgmt/_create_step_multi_table_form.html"

# Step 12
class DetailExpertEducationInfoAction(workflows.ReadOnlyModelAction):
    class Meta(object):
        name = u"教育信息"
        slug = u"detailexperteducationinfoaction"
        plus_action_name = u"+ 添加教育经历"
        model = models.Education
        fields = list(_EXPERTEDUCATIONFIELDS)
        table_format = [
            ['education_serial'],
            ['education_start', 'education_end'],
            ['education_country', 'education_yuanxiaomingcheng'],
            ['education_zhuanye'],
            ['education_xueli', 'education_xuewei'],
            ['education_peixunjinxiu'],
            ['education_zhidaojiaoshi'],
        ]
        output = EXPERTEDUCATIONFIELDS0
        maxslices = MAX_EXPERTEDUCATION_SLICES

# Step 12
class DetailExpertEducationInfo(NoVerifyContributes, workflows.Step):
    action_class = DetailExpertEducationInfoAction
    contributes = EXPERTEDUCATIONFIELDS
    template_name = "admin/expertmgmt/_create_step_multi_table_form.html"

# Step 13
class DetailExpertPartTimeJobInfoAction(workflows.ReadOnlyModelAction):
    class Meta(object):
        name = u"学术兼职"
        slug = u"detailexpertparttimejobinfoaction"
        plus_action_name = u"+ 添加学术兼职经历"
        model = models.PartTimeJob
        fields = list(_EXPERTPARTTIMEJOBFIELDS)
        table_format = [
            ['parttimejob_serial', 'parttimejob_sessionid'],
            ['parttimejob_start', 'parttimejob_end'],
            ['parttimejob_danwei', 'parttimejob_zhiwu'],
        ]
        output = EXPERTPARTTIMEJOBFIELDS0
        maxslices = MAX_EXPERTPARTTIMEJOB_SLICES

# Step 13
class DetailExpertPartTimeJobInfo(NoVerifyContributes, workflows.Step):
    action_class = DetailExpertPartTimeJobInfoAction
    contributes = EXPERTPARTTIMEJOBFIELDS
    template_name = "admin/expertmgmt/_create_step_multi_table_form.html"

# Step 14
class DetailExpertReviewHistoryInfoAction(workflows.ReadOnlyModelAction):
    class Meta(object):
        name = u"学术评审"
        slug = u"detailexpertreviewhistoryinfoaction"
        plus_action_name = u"+ 添加学术评审信息"
        model = models.ReviewHistory
        fields = list(_EXPERTREVIEWHISTORYFIELDS)
        table_format = [
            ['reviewhistory_serial'],
            ['reviewhistory_start', 'reviewhistory_end'],
            ['reviewhistory_weituojigou'],
            ['reviewhistory_content'],
        ]
        output = EXPERTREVIEWHISTORYFIELDS0
        maxslices = MAX_EXPERTREVIEWHISTORY_SLICES

# Step 14
class DetailExpertReviewHistoryInfo(NoVerifyContributes, workflows.Step):
    action_class = DetailExpertReviewHistoryInfoAction
    contributes = EXPERTREVIEWHISTORYFIELDS
    template_name = "admin/expertmgmt/_create_step_multi_table_form.html"

# Step 15
class DetailExpertXiangmuInfoAction(workflows.ReadOnlyModelAction):
    class Meta(object):
        name = u"承担项目情况"
        slug = u"detaileexpertxiangmuinfoaction"
        plus_action_name = u"+ 添加项目信息"
        model = models.XiangmuInfo
        fields = list(_EXPERTXIANGMUINFOFIELDS)
        table_format = [
            ['xiangmuinfo_serial'],
            ['xiangmuinfo_start', 'xiangmuinfo_end'],
            ['xiangmuinfo_name', 'xiangmuinfo_jibie'],
            ['xiangmuinfo_paiming', 'xiangmuinfo_bianhao'],
            ['xiangmuinfo_zizhuleibie', 'xiangmuinfo_jingfei'],
        ]
        output = EXPERTXIANGMUINFOFIELDS0
        maxslices = MAX_EXPERTXIANGMUINFO_SLICES

# Step 15
class DetailExpertXiangmuInfo(NoVerifyContributes, workflows.Step):
    action_class = DetailExpertXiangmuInfoAction
    contributes = EXPERTXIANGMUINFOFIELDS
    template_name = "admin/expertmgmt/_create_step_multi_table_form.html"

# Step 16
class DetailExpertAttachmentInfoAction(workflows.ReadOnlyModelAction, FillExpertAttachmentInfoAction):
    class Meta(object):
        name = u"附件"
        slug = u"detailexpertattachmentinfoaction"
        help_text_template = "admin/expertmgmt/_attachment_help.html"
        plus_action_name = u"+ 添加附件"
        model = models.Attachment
        fields = list(_EXPERTATTACHMENTFIELDS)
        table_format = [
            ['attachment_serial'],
            ['attachment_name', 'attachment_type'],
            ['attachment_file'],
        ]
        output = EXPERTATTACHMENTFIELDS0
        maxslices = MAX_EXPERTATTACHMENT_SLICES


# Step 16
class DetailExpertAttachmentInfo(NoVerifyContributes, workflows.Step):
    action_class = DetailExpertAttachmentInfoAction
    contributes = EXPERTATTACHMENTFIELDS
    template_name = "admin/expertmgmt/_create_step_multi_table_form.html"


# Entry
class DetailExpertRecord(workflows.Workflow):
    slug = "detailexpert"
    name = u"查看专家信息"
    finalize_button_name = ""
    success_url = "horizon:admin:expertmgmt:index"
    multipart = True

    default_steps = (DetailUserAccountInfo,
                     DetailBasicInfo,
                     DetailBankAccountInfo,
                     DetailOrganizationInfo,
                     DetailHighestEducation,
                     DetailOtherInfo,
                     DetailAcademicResearchInfo,
                     DetailExpertTitleInfo,
                     DetailExpertClassInfo,
                     DetailExpertDomainInfo,
                     DetailExpertFormalJobInfo,
                     DetailExpertEducationInfo,
                     DetailExpertPartTimeJobInfo,
                     DetailExpertReviewHistoryInfo,
                     DetailExpertXiangmuInfo,
                     DetailExpertAttachmentInfo,
                    )

    def handle(self, request, context):
        return True

