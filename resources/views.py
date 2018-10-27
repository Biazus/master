from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from .models import Resource, ResourceType


class ResourceCreate(CreateView):
    model = Resource
    success_url = reverse_lazy('resources:resource_list')
    fields = ['name', 'price', 'collaborative', 'open_source', 'available_web', 'multiplatform',]


class ResourceList(ListView):
    model = Resource


class ResourceUpdate(UpdateView):
    model = Resource
    success_url = reverse_lazy('resources:resource_list')
    fields = ['name', 'price', 'collaborative', 'open_source', 'available_web', 'multiplatform',]


class ResourceDelete(DeleteView):
    model = Resource
    success_url = reverse_lazy('resources:resource_list')


class ResourceTypeCreate(CreateView):
    model = ResourceType
    success_url = reverse_lazy('resources:resource_type_list')
    fields = ['name', ]


class ResourceTypeList(ListView):
    model = ResourceType


class ResourceTypeUpdate(UpdateView):
    model = ResourceType
    success_url = reverse_lazy('resources:resource_type_list')
    fields = ['name', ]


class ResourceTypeDelete(DeleteView):
    model = ResourceType
    success_url = reverse_lazy('resources:resource_type_list')
