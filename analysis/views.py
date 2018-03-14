from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView

# Create your views here.

class AnalysisCreate(CreateView):
    model = Analysis
    success_url = reverse_lazy('analysis:analysis_list')
    fields = []


class AnalysisList(ListView):
    model = Analysis
