from django.urls import path
from .views import *

urlpatterns = [
    path('', ViewStore.as_view(), name="store-view"),
    path('<int:pk>/add', cart_add_index, name='cart-add'),
    path('<int:pk>', ProductDetail.as_view(), name='product-detail'),
    path('cart', ViewCart.as_view(), name='cart-detail'),
    path('cart/<int:pk>/add', cart_plus, name='cart-plus'),
    path('cart/<int:pk>/delete', cart_minus, name='cart-minus'),
    path('checkout', CheckoutDetail.as_view(), name='checkout-detail'),


]