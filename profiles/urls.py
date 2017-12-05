from django.conf.urls import url
from profiles import views

urlpatterns = [
    # url(r'^$', views.process_upload, name='upload_form'),
    url(r'^process/$', views.ProcessList.as_view(), name='process_list'),
    url(r'^process/new$', views.ProcessCreate.as_view(), name='process_new'),
    url(r'^process/edit/(?P<pk>\d+)$', views.ProcessUpdate.as_view(), name='process_edit'),
    url(r'^process/delete/(?P<pk>\d+)$', views.ProcessDelete.as_view(), name='process_delete'),
    url(r'^process/edit/(?P<pk>\d+)/tasks$', views.TasksEdit.as_view(), name='tasks_edit'),
    url(r'^organization/$', views.OrganizationList.as_view(), name='organization_list'),
    url(r'^organization/new$', views.OrganizationCreate.as_view(), name='organization_new'),
    url(r'^organization/edit/(?P<pk>\d+)$', views.OrganizationUpdate.as_view(), name='organization_edit'),
    url(r'^organization/delete/(?P<pk>\d+)$', views.OrganizationDelete.as_view(), name='organization_delete'),

]
