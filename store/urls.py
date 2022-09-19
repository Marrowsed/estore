from django.urls import path
from .views import *

urlpatterns = [
    path('', ViewStore.as_view(), name="store-view"),
    path('<int:pk>/add', cart_add, name='cart-add'),
    path('<int:pk>', ProductDetail.as_view(), name='product-detail'),
    path('cart', ViewCart.as_view(), name='cart-detail'),

]