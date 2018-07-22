# -*- coding:utf-8 -*-
from collections import OrderedDict
import copy
import logging
import six
from horizon import exceptions
from horizon import forms
from horizon import messages
from horizon.utils import validators

from django.core.urlresolvers import reverse
from django import forms as django_forms
from django.forms import ValidationError  # noqa
from django.forms.widgets import HiddenInput  # noqa
from django import http
from django.http import QueryDict
from django.utils import timezone
from django.utils.encoding import force_text
from django.core import validators as django_validators

from openstack_dashboard import models
from openstack_dashboard.utils import expert_db_handle
from openstack_dashboard.utils import project_db_handle

from openstack_dashboard.dashboards.admin.expertmgmt import forms as expertmgmt_forms
from openstack_dashboard.dashboards.admin.expertmgmt.views import get_experts_data

LOG = logging.getLogger(__name__)

MAXREVIEWEXPERT = 100
REVIEWRESULTFIELDS = ['comments', 'comments_attachments', 'comments_on_comments']

def handle_check_project_state(expected_states):
    def wrapper1(func):
        def wrapper2(self, request, data, *args, **kwargs):
            projectid = data.get('id') or data.get('projectid')
            if not projectid:
                messages.error(request, u"项目状态错误，请刷新后重新提交")
                return False
            project = project_db_handle.GetProjectInstanceById(projectid)
            if not project:
                messages.error(request, u"项目状态错误，请刷新后重新提交")
                return False
            if not project.state in expected_states:
                messages.error(request, u"项目状态错误，请刷新后重新提交")
                return False
            if 'id' in data:
                data['id'] = project
            elif 'projectid' in data:
                data['projectid'] = project
            return func(self, request, data, *args, **kwargs)
        return wrapper2
    return wrapper1

class SearchForm(expertmgmt_forms.SearchForm):
    def __init__(self, request, *args, **kwargs):
        super(SearchForm, self).__init__(request, *args, **kwargs)
        param = project_db_handle.SEARCHPARAM
        self.fields['field1'].choices = [ (f, project_db_handle.SEARCHFIELDS_VALUE[f]) for f in param['field1_choices'] ]
        self.fields['field2'].choices = [ (f, project_db_handle.SEARCHFIELDS_VALUE[f]) for f in param['field2_choices'] ]

DOMAIN = {
     u"国家科技部领域": [u"数学", u"信息科学与系统科学", u"物理学"],
     u"国家基金委领域": [u"数理科学", u"化学科学", u"生命科学",],
 }

FIRST_TAGS = [(k, k) for k in DOMAIN]
SECOND_TAGS = [(k, [
      [v, v] for v in val
     ]) for k, val in DOMAIN.items()]

class SetRuleForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())
    # hangyefenlei = forms.CharField(max_length=255,
    #     label=u"行业分类", required=False)
    hangyefenlei = forms.CharField(max_length=32, choices=SECOND_TAGS, label=u"行业分类", required=False)
    age_min = forms.IntegerField(
        min_value=1, initial=25, max_value=150, label=u"年龄下限",
        help_text=u"请输入欲抽取评审专家的年龄下限（即年龄大于或等于该值）", required=False)
    age_max = forms.IntegerField(
        min_value=1, initial=65, max_value=150, label=u"年龄上限",
        help_text=u"请输入欲抽取评审专家的年龄上限（即年龄小于或等于该值）", required=False)
    huibirenyuan = forms.CharField(max_length=255, label=u"回避人员",
        help_text=u"填写回避专家姓名", required=False)
    huibidanwei = forms.CharField(max_length=255, label=u"回避单位",
        help_text=u"填写回避单位名称", required=False)
    chouqurenshu = forms.IntegerField(
        min_value=1, label=u"评审专家数量",
        help_text=u"请输入欲抽取评审专家的数量", required=True)
    exclude_same_org = forms.BooleanField(
        label=u"排除项目申报单位的专家", initial=True, required=True,
        help_text=u"为避免出现不公正评审，默认不抽取项目申报单位的专家",)

    field_order = ['id', 'hangyefenlei', 'zuigaoxueli', 'zuigaoxuewei']
    noborder = True
    plus_action_hidden = False
    model_fields = ['hangyefenlei']
    id_prefix = ''
    maxslices = 5

    def __str__(self):
        return force_text(self.name)

    def __init__(self, request, *args, **kwargs):
        super(SetRuleForm, self).__init__(request, *args, **kwargs)
        if self.maxslices and self.model_fields:
            tmp_fields = OrderedDict()
            for fname in self.model_fields:
                fi = self.fields[fname]
                for i in range(1, 1 + self.maxslices):
                    name = '%s%d' % (fname, i)
                    field = copy.deepcopy(fi)
                    tmp_fields[name] = field
            for name in tmp_fields:
                self.fields[name] = tmp_fields[name]
            for fname in self.model_fields:
                self.fields[fname].widget = forms.HiddenInput()
                self.fields[fname].noboder = True
        all_roles = [ d.get('name') for d in request.user.roles ]
        if 'admin' not in all_roles:
            self.fields['exclude_same_org'].disabled = True
        max_value = self.initial.get('chouqurenshu', 0)
        if max_value:
            f = self.fields['chouqurenshu']
            f.max_value = max_value
            extra_attrs = f.widget_attrs(f.widget)
            f.widget.attrs.update(extra_attrs)
            self.fields['chouqurenshu'].validators.append(
                django_validators.MaxValueValidator(max_value))

    def clean(self):
        data = super(SetRuleForm, self).clean()
        if data['age_min'] and data['age_max'] and data['age_min'] > data['age_max']:
            raise ValidationError(u"年龄下限必须小于年龄上限")

        for fname in self.model_fields:
            data[fname] = []
            for i in range(1, 1 + self.maxslices):
                name = '%s%d' % (fname, i)
                if data[name]:
                    data[fname].append(data[name])
            if not data[fname]:
                f = self.get_field_by_name(fname)
                s = u"%s为必填项，至少填写一个值" % f.label
                raise ValidationError(s)

        return data

    def visible_fields(self):
        model_fields = []
        for i in self.model_fields:
            model_fields.append(i)
            for j in range(1, 1 + self.maxslices):
                model_fields.append("%s%d" % (i, j))
        return [field for field in self if not field.is_hidden and not field.name in model_fields]

    def get_field_by_name(self, name):
        for field in self:
            if field.name == name:
                field.noboder = True
                return field
        return None

    def get_one_slice(self, curr_id, prev):
        oneslice = {}
        hidden = False
        has_value = False
        elements = []
        for i in self.model_fields:
            name = "%s%d" % (i, curr_id)
            field = self.get_field_by_name(name)
            elements.append(field)
            has_value = False
        oneslice['fields'] = elements
        oneslice['id'] = "%sslice_%s_%d" % (self.id_prefix, self.model_fields[0], curr_id)

        oneslice['has_value'] = has_value
        if prev:
            prev['next'] = oneslice['id']
            if prev['hidden']:
                hidden = True
            elif not prev['has_value']:
                hidden = True
            elif self.plus_action_hidden:
                hidden = True
        else:
            hidden = False
        if has_value:
            hidden = False
        oneslice['hidden'] = hidden
        if prev:
            if self.plus_action_hidden:
                prev['shownext'] = False
            else:
                prev['shownext'] = hidden
        return oneslice

    def get_titlefields(self):
        result = []
        for i in self.model_fields:
            result.append(self.get_field_by_name(i))
        return result

    def get_slices(self):
        slices = []
        prev = None
        for i in range(1, 1 + self.maxslices):
            oneslice = self.get_one_slice(i, prev)
            slices.append(oneslice)
            prev = oneslice
        if prev:
            prev['next'] = None
            prev['shownext'] = False
        return slices

    @handle_check_project_state(['waitfor_setrule'])
    def handle(self, request, data):
        chouqurenshu = int(data['chouqurenshu'])
        project = data['id']
        hangyefenlei = data['hangyefenlei']
        age_min = data['age_min']
        age_max = data['age_max']
        exclude_danwei = data['huibidanwei']
        exclude_renyuan = data['huibirenyuan']
        exclude_same_org = data['exclude_same_org']
        zuigaoxueli = data['zuigaoxueli']
        zuigaoxuewei = data['zuigaoxuewei']

        if not isinstance(hangyefenlei, list) or not hangyefenlei:
            messages.error(request, u"行业分类为空，设置抽取规则失败")
            return False
        excluders = []
        if exclude_same_org:
            excluders.append({'var': 'suozaidaiwei', 'operator': 'exact', 'words': project.shenbaodanwei})
        if exclude_danwei:
            if not (exclude_same_org and project.shenbaodanwei == exclude_danwei):
                excluders.append({'var': 'suozaidaiwei', 'operator': 'exact', 'words': exclude_danwei})
        if exclude_renyuan:
            excluders.append({'var': 'expertname', 'operator': 'exact', 'words': exclude_renyuan})

        filters = [{'var': 'state', 'operator': 'exact', 'words': 'approved'}]
        if age_min:
            expert_db_handle.filter_adapt(filters, 'age', 'gte', age_min)
        if age_max:
            expert_db_handle.filter_adapt(filters, 'age', 'lte', age_max)
        if zuigaoxueli:
            expert_db_handle.filter_adapt(filters, 'zuigaoxueli', 'exact', zuigaoxueli)
        if zuigaoxuewei:
            expert_db_handle.filter_adapt(filters, 'zuigaoxuewei', 'exact', zuigaoxuewei)

        experts = expert_db_handle.DomainBasedQueryExperts(
            hangyefenlei, filters=filters, excluders=excluders)
        total_num = len(experts)
        if total_num == 0:
            messages.error(request, u"未能查询到适合的候选专家，请重新设置条件")
            return False
        project_db_handle.CleanCandidates(project)
        (project, _has_in_pool, has_in_project, has_unavailable) = \
            project_db_handle.AddCandidates(project, experts)
        has_in_project_num = len(has_in_project)
        has_unavailable_num = len(has_unavailable)
        candidates_num = total_num - has_in_project_num - has_unavailable_num
        if candidates_num <= 0:
            messages.error(request,
                u"符合条件的%d位专家均已被抽取或无法参与评审，请重新设置条件" % has_in_project_num)
            return False
        bindrec = project_db_handle.CreateBindRecord(project, data, chouqurenshu)
        project_db_handle.AlreadySetRule(project)
        project_db_handle.UpdateCandidateNum(bindrec, candidates_num)
        messages.success(request, u"根据抽取规则，找到%d位候选人" % candidates_num)
        return True

    class Meta(object):
        name = 'setruleform'
        model = models.Expert
        fields = ['zuigaoxueli', 'zuigaoxuewei']

class StartReviewForm(forms.SelfHandlingForm):
    id = forms.CharField(widget=forms.HiddenInput())
    projectname = forms.CharField(label=u"项目名称",
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    description = forms.CharField(max_length=65535, widget=forms.Textarea(
        attrs={'rows': 10}),
        label=u"项目评审说明", required=False)

    no_description_field = True

    @handle_check_project_state(['kickoff'])
    def handle(self, request, data):
        project = data['id']
        if data['description']:
            project = project_db_handle.SaveStartReviewDescription(project, data['description'])
        project = project_db_handle.StartReviewProject(project)
        msg = u"项目'%s'开始评审" % data['projectname']
        messages.success(request, msg)
        return True

class RandomBindForm(forms.SelfHandlingForm):
    id = forms.CharField(widget=forms.HiddenInput())
    projectname = forms.CharField(label=u"项目名称",
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    chouqurenshu = forms.IntegerField(label=u"评审专家数量", min_value=1,
        help_text=u"请选择欲抽取的评审专家数量",)
    reason = forms.CharField(label=u"抽取说明", max_length=65535, required=True,
        widget=forms.Textarea(attrs={'rows': 10}))

    def __init__(self, request, *args, **kwargs):
        super(RandomBindForm, self).__init__(request, *args, **kwargs)
        max_value = self.initial['chouqurenshu']
        if max_value:
            f = self.fields['chouqurenshu']
            f.max_value = max_value
            extra_attrs = f.widget_attrs(f.widget)
            f.widget.attrs.update(extra_attrs)
            self.fields['chouqurenshu'].validators.append(
                django_validators.MaxValueValidator(max_value))

    @handle_check_project_state(['waitfor_bind'])
    def handle(self, request, data):
        project = data['id']
        chouqurenshu = data['chouqurenshu']
        reason = data['reason']
        binded_experts = project_db_handle.RandomBindExpert(project, chouqurenshu)
        binded_experts_num = len(binded_experts)
        if binded_experts_num:
            msg = u"以下专家被选中加入项目%s的评审专家列表：%s" % (
                  data['projectname'], expert_db_handle.get_all_expert_names(binded_experts))
            messages.success(request, msg)
        if binded_experts_num != chouqurenshu:
            msg = u"指定随机抽取%d名专家，实际抽取%d名专家" % (
                  chouqurenshu, binded_experts_num)
            messages.error(request, msg)
        if binded_experts_num:
            #project = project_db_handle.GetProjectInstanceById(projectid)
            project_db_handle.UpdateReviewerNum(project.current_bindrec,
                                                binded_experts_num,
                                                reason)
            project_db_handle.BindedExperts(project)
        return binded_experts_num

class CommentExpertReviewForm(forms.SelfHandlingForm):
    projectid = forms.CharField(widget=forms.HiddenInput())
    expertid = forms.CharField(widget=forms.HiddenInput())
    projectname = forms.CharField(label=u"项目名称",
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    expertname = forms.CharField(label=u"专家姓名",
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    comments = forms.CharField(max_length=65535, widget=forms.Textarea(
        attrs={'rows': 20}), help_text=u"评论最多65535字节，约3.2万字",
        label=u"评价内容", required=True)

    no_description_field = True

    @handle_check_project_state(['finished'])
    def handle(self, request, data):
        project = data['projectid']
        expertid = data['expertid']
        _comments = data['comments']
        username = self.request.user.username
        now = timezone.now().isoformat()
        comments = u"[%s]用户[%s]：提交评论：\n%s" % (now, username, _comments)
        project_db_handle.CommentExpertReview(project, expertid, comments)
        return True

class ViewReviewResultForm(forms.ModelForm):
    projectid = forms.CharField(widget=forms.HiddenInput())
    expertid = forms.CharField(widget=forms.HiddenInput())
    projectname = forms.CharField(label=u"项目名称",
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    expertname = forms.CharField(label=u"专家姓名",
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    no_description_field = True
    field_order = ['projectid', 'expertid', 'projectname', 'expertname'] + REVIEWRESULTFIELDS

    class Meta(object):
        model = models.Reviewer
        fields = REVIEWRESULTFIELDS

    def __init__(self, request, *args, **kwargs):
        super(ViewReviewResultForm, self).__init__(request, *args, **kwargs)
        for f in REVIEWRESULTFIELDS:
            self.fields[f].disabled = True

    def handle(self, request, data):
        return True

