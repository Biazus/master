from django.http import HttpResponse
from .forms import TaskFormSet
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.views import View
from django.shortcuts import redirect, render

from .models import Process, Task, Organization
from .services import ServicesProfiles


class ProcessList(ListView):
    model = Process


class ProcessCreate(CreateView):
    model = Process
    success_url = reverse_lazy('profiles:process_list')
    fields = ['name', 'raw_file', 'organization']

    def form_valid(self, form):
        response = super(ProcessCreate, self).form_valid(form)
        ServicesProfiles().parse_file(form.instance)
        return response


class ProcessUpdate(UpdateView):
    model = Process
    success_url = reverse_lazy('profiles:process_list')
    fields = ['name', 'organization']

    def post(self, request, *args, **kwargs):
        instance = Process.objects.get(id=kwargs.get('pk'))
        if 'recommend' in request.POST:
            service = ServicesProfiles()
            test = [task for task in instance.task_set.all()]
            training = [task for task in Task.objects.filter(process__organization=instance.organization) if
                    task not in test]
            service.recommend(test, training)
        else:
            return super(ProcessUpdate, self).post(self, request, *args, **kwargs)
        return redirect('profiles:process_list')


class ProcessDelete(DeleteView):
    model = Process
    success_url = reverse_lazy('profiles:process_list')


class OrganizationCreate(CreateView):
    model = Organization
    success_url = reverse_lazy('profiles:organization_list')
    fields = ['name', 'suite']


class OrganizationList(ListView):
    model = Organization


class OrganizationUpdate(UpdateView):
    model = Organization
    success_url = reverse_lazy('profiles:organization_list')
    fields = ['name', 'suite']


class OrganizationDelete(DeleteView):
    model = Organization
    success_url = reverse_lazy('profiles:organization_list')


class CrossValidation(View):
    def get(self, request, *args, **kwargs):
        service = ServicesProfiles()
        pk = kwargs.get('pk')
        accuracy = service.cross_validation(pk)
        org = Organization.objects.get(id=pk)
        org.accuracy = accuracy
        org.save()
        return redirect('profiles:organization_edit', pk=pk)


class TasksEdit(View):
    template = 'profiles/tasks_edit.html'
    form_class = TaskFormSet

    def get(self, request, *args, **kwargs):
        form = self.form_class(queryset=Task.objects.filter(process_id=kwargs.pop('pk')))
        return render(request, self.template, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profiles:process_edit', pk=self.kwargs.get('pk'))
        return render(request, self.template, {'form': form})
