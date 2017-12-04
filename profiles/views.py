from .forms import TaskFormSet
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.views import View
from django.shortcuts import redirect, render

from .models import Process, Task
from .services import ServicesProfiles

# def process_upload(request):
#     message = ''
#     if request.method == 'POST':
#         form = ProcessForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             message = 'Sucess!'
#         else:
#             message = 'There was an error on your request.'
#     else:
#         form = ProcessForm()
#
#     return render(request, 'process.html', {
#         'form': form,
#         'feedback_to_user': message
#     })


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


class ProcessDelete(DeleteView):
    model = Process
    success_url = reverse_lazy('profiles:process_list')


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
            return redirect('profiles:process_list')
        return render(request, self.template, {'form': form})
