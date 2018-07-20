# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
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

from django.conf.urls import url

from openstack_dashboard.dashboards.admin.projectmgmt import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    # Normal Project Manage
    url(r'^searchproject$', views.SearchProjectView.as_view(), name='searchproject'),
    url(r'^createproject$', views.CreateProjectView.as_view(), name='createproject'),
    url(r'^(?P<projectid>[^/]+)/updateproject$', views.UpdateProjectView.as_view(), name='updateproject'),
    url(r'^(?P<projectid>[^/]+)/viewproject$', views.ViewProjectView.as_view(), name='viewproject'),

    # Bind Reviewer
    url(r'^(?P<projectid>[^/]+)/setrule$', views.SetRuleView.as_view(), name='setrule'),
    url(r'^(?P<projectid>[^/]+)/managecandidate$', views.ManageCandidateView.as_view(), name='managecandidate'),
    url(r'^(?P<projectid>[^/]+)/managecandidate2$', views.ManageCandidate2View.as_view(), name='managecandidate2'),
    url(r'^(?P<projectid>[^/]+)/searchcandidate2$', views.SearchCandidate2View.as_view(), name='searchcandidate2'),
    url(r'^(?P<projectid>[^/]+)/managereviewer$', views.ManageReviewerView.as_view(), name='managereviewer'),
    url(r'^(?P<projectid>[^/]+)/managereviewer2$', views.ManageReviewer2View.as_view(), name='managereviewer2'),
    url(r'^(?P<projectid>[^/]+)/viewreviewer$', views.ViewReviewerView.as_view(), name='viewreviewer'),
    url(r'^(?P<projectid>[^/]+)/randombind$', views.RandomBindView.as_view(), name='randombind'),
    url(r'^(?P<projectid>[^/]+)/startreview$', views.StartReviewView.as_view(), name='startreview'),

    # Manage Review Result
    url(r'^(?P<projectid>[^/]+)/managereviewresult$', views.ManageReviewResultView.as_view(), name='managereviewresult'),
    url(r'^(?P<projectid>[^/]+)/(?P<expertid>[^/]+)/viewreviewresult$', views.ViewReviewResultView.as_view(), name='viewreviewresult'),
    url(r'^(?P<projectid>[^/]+)/(?P<expertid>[^/]+)/commentreviewresult', views.CommentExpertReviewView.as_view(), name='commentreviewresult'),
]

