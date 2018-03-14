from django.conf.urls import url
from analysis import views

urlpatterns = [
     url(r'^analysis/$', views.AnalysisList.as_view(), name='analysis_list'),
     url(r'^analysis/new$', views.AnalysisCreate.as_view(), name='analysis_new'),
]
