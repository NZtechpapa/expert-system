# -*- coding:utf-8 -*-
import logging

from horizon import exceptions
from horizon import forms
from horizon import messages
from horizon.utils import validators

from django.core.urlresolvers import reverse
from django.forms import ValidationError  # noqa
from django.forms.widgets import HiddenInput  # noqa
from django import http
from django.http import QueryDict

from openstack_dashboard.utils import expert_db_handle

LOG = logging.getLogger(__name__)

class SearchForm(forms.SelfHandlingForm):
    field1 = forms.ChoiceField(
        label=u"字段一",
        required=True,
        help_text=u"搜索字段名称",
        )

    oper1 = forms.ChoiceField(
        label=u"运算符",
        required=True,
        help_text=u"搜索字段和值之间的关系",
        )

    value1 = forms.CharField(max_length=255,
        label=u"值", required=True)

    mainop = forms.ChoiceField(
        label=u"逻辑关系",
        required=False,
        help_text=u"搜索条件一和搜索条件二之间的逻辑关系",
        widget=forms.ThemableSelectWidget(attrs={
            'class': 'switchable',
            'data-slug': 'mainop',
        }),)

    field2 = forms.ChoiceField(
        label=u"字段二",
        required=False,
        help_text=u"搜索字段名称",
        widget=forms.ThemableSelectWidget(attrs={
            'class': 'switched',
            'data-switch-on': 'mainop',
            'data-mainop-and': u"字段二",
            'data-mainop-or': u"字段二",
            'data-mainop-exclude': u"字段二",
        }),)

    oper2 = forms.ChoiceField(
        label=u"运算符",
        required=False,
        help_text=u"搜索字段和值之间的关系",
        widget=forms.ThemableSelectWidget(attrs={
            'class': 'switched',
            'data-switch-on': 'mainop',
            'data-mainop-and': u"运算符",
            'data-mainop-or': u"运算符",
            'data-mainop-exclude': u"运算符",
        }),)

    value2 = forms.CharField(max_length=255,
        label=u"值", required=False,
        widget=forms.TextInput(attrs={
            'class': 'switched',
            'data-switch-on': 'mainop',
            'data-mainop-and': u"值",
            'data-mainop-or': u"值",
            'data-mainop-exclude': u"值",
        }),)

    def __init__(self, request, *args, **kwargs):
        super(SearchForm, self).__init__(request, *args, **kwargs)
        param = expert_db_handle.SEARCHPARAM
        self.fields['field1'].choices = [ (f, expert_db_handle.SEARCHFIELDS_VALUE[f]) for f in param['field1_choices'] ]
        self.fields['oper1'].choices = [ (o, expert_db_handle.OPERATORS_VALUE[o]) for o in param['oper1_choices'] ]
        self.fields['field2'].choices = [ (f, expert_db_handle.SEARCHFIELDS_VALUE[f]) for f in param['field2_choices'] ]
        self.fields['oper2'].choices = [ (o, expert_db_handle.OPERATORS_VALUE[o]) for o in param['oper2_choices'] ]
        self.fields['mainop'].choices = [ ('', '') ] + [ (m, expert_db_handle.MAINOPERATORS_VALUE[m]) for m in param['mainop_choices'] ]

        if not 'initial' in kwargs:
            return
        else:
            initial = kwargs['initial']

        self.initial['field1'] = initial['field1']
        self.initial['oper1'] = initial['oper1']
        self.initial['value1'] = initial['value1']
        self.initial['field2'] = initial['field2']
        self.initial['oper2'] = initial['oper2']
        self.initial['value2'] = initial['value2']
        self.initial['mainop'] = initial['mainop']

    def clean(self):
        data = super(SearchForm, self).clean()
        if not data['mainop']:
            for key in ['field2', 'oper2', 'value2', 'mainop']:
                if key in data.keys():
                    del data[key]
        return data

    def get_search_params(self, data):
        q = QueryDict('', mutable=True)
        q['field1'] = data['field1']
        q['oper1'] = data['oper1']
        q['value1'] = data['value1']
        if 'mainop' in data and 'field2' in data and 'oper2' in data and 'value2' in data:
            if data['mainop'] and data['field2'] and data['oper2'] and data['value2']:
                q['mainop'] = data['mainop']
                q['field2'] = data['field2']
                q['oper2'] = data['oper2']
                q['value2'] = data['value2']
        return q

    def handle(self, request, data):
        return self.get_search_params(data)
