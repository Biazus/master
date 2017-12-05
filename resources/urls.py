from django.conf.urls import url
from resources import views

urlpatterns = [
     url(r'^product/$', views.ProductList.as_view(), name='product_list'),
     url(r'^product/new$', views.ProductCreate.as_view(), name='product_new'),
     url(r'^product/edit/(?P<pk>\d+)$', views.ProductUpdate.as_view(), name='product_edit'),
     url(r'^product/delete/(?P<pk>\d+)$', views.ProductDelete.as_view(), name='product_delete'),
]
