from django.conf.urls import url, include
from django.contrib import admin
from core import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
