from django.shortcuts import redirect
from django.views import View
from .utils import *


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
    """
    Add Products in Cart
    """
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
    """
    Delete Products in Cart
    """
    product = Product.objects.get(id=pk)
    order, created = Order.objects.get_or_create(
        customer=request.user.customer,
        complete=False
    )
    cart, created = Cart.objects.get_or_create(
        product=product,
        order=order,
    )
    product.quantity += 1
    product.save()
    if cart.quantity >= 1:
        cart.delete()
        order.delete()
    else:
        cart.quantity -= 1
        cart.save()
    return redirect('cart-detail')


class CheckoutDetail(View):

    def get(self, request, *args, **kwargs):
        view = ViewCheckout.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostCheckout.as_view()
        return view(request, *args, **kwargs)
