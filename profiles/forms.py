from django.forms import modelformset_factory
from django import forms
from .models import Process, Task


class ProcessForm(forms.ModelForm):
    class Meta:
        model = Process
        fields = ('name', 'organization', 'raw_file')


TaskFormSet = modelformset_factory(Task, fields=('label', 'id', 'task_type', 'application_type', ), extra=0)
