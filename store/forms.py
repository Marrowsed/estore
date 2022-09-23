from django.forms import ModelForm
from .models import *


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"


class CheckoutForm(ModelForm):
    class Meta:
        model = Checkout
        fields = "__all__"
