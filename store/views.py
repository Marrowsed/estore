from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView
from django.contrib import messages
from django.views.generic import DetailView, ListView

from .forms import ProductForm
from .models import *


# Create your views here.

class ViewStore(ListView):
    template_name = 'estore/index.html'
    model = Product

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['cart'] = Cart.objects.all()
        return context

    def get_success_url(self):
        return reverse('store-view')


def cart_add_index(request, pk):
    product = Product.objects.get(id=pk)
    order, created = Order.objects.get_or_create(
        customer=request.user.customer,
        complete=False
    )
    cart, created = Cart.objects.get_or_create(
        product=product,
        order=order,
    )
    cart.quantity += 1
    cart.save()
    product.quantity -= 1
    product.save()
    return redirect("store-view")


class ViewProduct(DetailView):
    template_name = 'estore/product.html'
    model = Product

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Product, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shipping'] = ShippingOption.objects.all()
        return context


class PostProduct(SingleObjectMixin, FormView):
    template_name = 'estore/product.html'
    model = Product
    form_class = ProductForm

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        order, created = Order.objects.get_or_create(
            customer=request.user.customer,
            complete=False
        )
        cart, created = Cart.objects.get_or_create(
            product=self.object,
            order=order,
        )
        if 'add-cart' in request.POST:
            if cart.quantity < self.object.quantity:
                self.object.quantity -= 1
                self.object.save()
                cart.quantity += 1
                cart.save()
            elif cart.quantity == 0:
                cart.delete()
            else:
                messages.error(request, "Can't put item in cart !", extra_tags='alert alert-danger')

        if 'delete-cart' in request.POST:
            order.delete()
            if cart.quantity == 0:
                cart.delete()
            else:
                cart.quantity -= 1
                cart.save()
                self.object.quantity += 1
                self.object.save()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('product-detail', kwargs={'pk': self.object.pk})


class ProductDetail(View):

    def get(self, request, *args, **kwargs):
        view = ViewProduct.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostProduct.as_view()
        return view(request, *args, **kwargs)


class ViewCart(ListView):
    template_name = 'estore/cart.html'
    model = Cart

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart.objects.all()
        customer = self.request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        context['order_items'] = order.get_cart_items
        context['order_total'] = order.get_cart_total
        return context


def cart_plus(request, pk):
    product = Product.objects.get(id=pk)
    order, created = Order.objects.get_or_create(
        customer=request.user.customer,
        complete=False
    )
    cart, created = Cart.objects.get_or_create(
        product=product,
        order=order,
    )
    if product.quantity > 0:
        cart.quantity += 1
        cart.save()
        product.quantity -= 1
        product.save()
    else:
        messages.error(request, "Item out of stock !", extra_tags='alert alert-danger')
    return redirect('cart-detail')


def cart_minus(request, pk):
    product = Product.objects.get(id=pk)
    order, created = Order.objects.get_or_create(
        customer=request.user.customer,
        complete=False
    )
    cart, created = Cart.objects.get_or_create(
        product=product,
        order=order,
    )
    if cart.quantity == 0:
        cart.delete()
    else:
        cart.quantity -= 1
        cart.save()
        product.quantity += 1
        product.save()
    return redirect('cart-detail')

class ViewCheckout(ListView):
    template_name = 'estore/checkout.html'
    model = Cart

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart.objects.all()
        context['shippingOption'] = ShippingOption.objects.all()
        customer = self.request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        context['order_items'] = order.get_cart_items
        context['order_total'] = order.get_cart_total
        return context


