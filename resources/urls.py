from django.conf.urls import url
from resources import views

urlpatterns = [
     url(r'^resource/$', views.ResourceList.as_view(), name='resource_list'),
     url(r'^resource/new$', views.ResourceCreate.as_view(), name='resource_new'),
     url(r'^resource/edit/(?P<pk>\d+)$', views.ResourceUpdate.as_view(), name='resource_edit'),
     url(r'^resource/delete/(?P<pk>\d+)$', views.ResourceDelete.as_view(), name='resource_delete'),

     url(r'^resource_type/$', views.ResourceTypeList.as_view(), name='resource_type_list'),
     url(r'^resource_type/new$', views.ResourceTypeCreate.as_view(), name='resource_type_new'),
     url(r'^resource_type/edit/(?P<pk>\d+)$', views.ResourceTypeUpdate.as_view(), name='resource_type_edit'),
     url(r'^resource_type/delete/(?P<pk>\d+)$', views.ResourceTypeDelete.as_view(),
         name='resource_type_delete'),
]
