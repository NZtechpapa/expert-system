from django.conf.urls import url

from openstack_dashboard.dashboards.project.review import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<projectid>[^/]+)/viewreview$', views.ViewReviewContentView.as_view(), name='viewreview'),
    url(r'^(?P<projectid>[^/]+)/doreview$', views.FillReviewContentView.as_view(), name='doreview'),
    url(r'^(?P<projectid>[^/]+)/updatereview$', views.FillReviewContentView.as_view(), name='updatereview'),
]

