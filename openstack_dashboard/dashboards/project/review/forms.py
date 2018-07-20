# -*- coding:utf-8 -*-
import logging

from horizon import exceptions
from horizon import forms
from horizon import messages
from horizon.utils import validators

from django import forms as django_forms
from django.core.urlresolvers import reverse
from django.forms.utils import from_current_timezone
from openstack_dashboard import models
from openstack_dashboard.utils import expert_db_handle
from openstack_dashboard.utils import project_db_handle

LOG = logging.getLogger(__name__)

class FillReviewContentForm(forms.ModelForm):
    id = forms.CharField(label="ID", required=True, widget=forms.HiddenInput())
    projectid = forms.CharField(widget=forms.HiddenInput(), required=True)
    no_description_field = True

    class Meta(object):
        model = models.Reviewer
        fields = ['comments', 'comments_attachments',]

    def handle(self, request, data):
        redirect = reverse("horizon:settings:user:index")
        comments_attachments = data['comments_attachments']
        expertid = expert_db_handle.get_expertid_from_keystone_user(
            request, redirect=redirect)
        try:
            project_db_handle.UpdateReviewComments(
                data['projectid'], expertid,
                data['comments'],
                comments_attachments)
        except Exception as e:
            exceptions.handle(request,
                              e.message,
                              redirect=redirect)

        return True

class ViewReviewContentForm(forms.ModelForm):
    id = forms.CharField(label="ID", required=True, widget=forms.HiddenInput())
    projectid = forms.CharField(widget=forms.HiddenInput(), required=True)
    no_description_field = True
    class Meta(object):
        model = models.Reviewer
        fields = ['comments', 'comments_attachments',]

    def __init__(self, request, *args, **kwargs):
        super(ViewReviewContentForm, self).__init__(request, *args, **kwargs)
        self.fields["comments"].disabled = True
        self.fields["comments_attachments"].disabled = True

    def handle(self, request, data):
        return True
