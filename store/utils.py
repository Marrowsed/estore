import datetime
import random

from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, ListView, FormView
from django.urls import reverse
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages

from store.forms import *
from store.models import *


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
            self.object.quantity += 1
            self.object.save()
            if cart.quantity >= 1:
                cart.delete()
                order.delete()
            else:
                cart.quantity -= 1
                cart.save()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('product-detail', kwargs={'pk': self.object.pk})


class ViewCheckout(ListView):
    template_name = 'estore/checkout.html'
    model = Checkout

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart.objects.all()
        context['shippingOption'] = ShippingOption.objects.all()
        customer = self.request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        context['order_items'] = order.get_cart_items
        context['order_total'] = order.get_cart_total
        return context


class PostCheckout(SingleObjectMixin, FormView):
    template_name = 'estore/checkout.html'
    model = Checkout

    def post(self, request, *args, **kwargs):
        customer = self.request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cart, created = Cart.objects.get_or_create(order=order)
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = get_object_or_404(Order, pk=order.pk)
        shipping = self.request.POST.get('shippingOption')
        shipping_option = ShippingOption.objects.get(name=shipping)
        cart.delete()
        order.complete = True
        order.transaction_id = datetime.datetime.now().timestamp()
        order.save()
        Checkout.objects.create(customer=customer,
                                order=order,
                                shipping_option=shipping_option,
                                address=self.request.POST.get('address'),
                                city=self.request.POST.get('city'),
                                state=self.request.POST.get('state'),
                                zipcode=self.request.POST.get('zip')
                                )
        super().post(request, *args, **kwargs)
        return redirect('store-view')

    def get_success_url(self):
        return reverse('store-view')
