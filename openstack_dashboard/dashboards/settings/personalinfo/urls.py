from django.conf.urls import url

from openstack_dashboard.dashboards.settings.personalinfo import views

urlpatterns = [
    url(r'^$', views.DetailView.as_view(), name='index'),
    url(r'^detail$', views.DetailView.as_view(), name='detail'),
    url(r'^update$', views.UpdateView.as_view(), name='update'),
]

