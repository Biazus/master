from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from .models import Product


class ProductCreate(CreateView):
    model = Product
    success_url = reverse_lazy('resources:product_list')
    fields = ['name', 'price']


class ProductList(ListView):
    model = Product


class ProductUpdate(UpdateView):
    model = Product
    success_url = reverse_lazy('resources:product_list')
    fields = ['name', 'price']


class ProductDelete(DeleteView):
    model = Product
    success_url = reverse_lazy('resources:product_list')