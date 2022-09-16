from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator

from .forms import ProductForm
from .models import *
from django.views.generic import DetailView


# Create your views here.

def store(request):
    product = Product.objects.all()
    ctx = {'products': product}
    return render(request, 'estore/index.html', ctx)


class ViewProduct(DetailView):
    template_name = 'estore/product.html'
    model = Product

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Product, pk=pk)
