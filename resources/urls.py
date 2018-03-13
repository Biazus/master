from django.conf.urls import url
from resources import views

urlpatterns = [
     url(r'^product/$', views.ProductList.as_view(), name='product_list'),
     url(r'^product/new$', views.ProductCreate.as_view(), name='product_new'),
     url(r'^product/edit/(?P<pk>\d+)$', views.ProductUpdate.as_view(), name='product_edit'),
     url(r'^product/delete/(?P<pk>\d+)$', views.ProductDelete.as_view(), name='product_delete'),

     url(r'^resource_type/$', views.ResourceTypeList.as_view(), name='resource_type_list'),
     url(r'^resource_type/new$', views.ResourceTypeCreate.as_view(), name='resource_type_new'),
     url(r'^resource_type/edit/(?P<pk>\d+)$', views.ResourceTypeUpdate.as_view(), name='resource_type_edit'),
     url(r'^resource_type/delete/(?P<pk>\d+)$', views.ResourceTypeDelete.as_view(),
         name='resource_type_delete'),
]
