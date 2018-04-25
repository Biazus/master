from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy

from profiles.services import ServicesProfiles
from .models import Analysis


class AnalysisCreate(CreateView):
    model = Analysis
    success_url = reverse_lazy('analysis:analysis_list')
    fields = []


class AnalysisList(ListView):
    model = Analysis


class CrossValidation(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')
