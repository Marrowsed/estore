from django.urls import path
from .views import *

urlpatterns = [
    path('', store, name="store-view"),
    path('<str:pk>', ViewProduct.as_view(), name='product-detail')
]