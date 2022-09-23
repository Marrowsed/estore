from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    digital = models.BooleanField(default=False, null=True, blank=True)
    description = models.TextField()
    quantity = models.IntegerField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        """
        If there's no image, show nothing
        """
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True, unique=True)

    def __str__(self):
        return f"Order Number: {self.id} - Transaction ID: {self.transaction_id}"

    @property
    def get_cart_total(self):
        """
        Return total value inside the cart
        """
        cart = self.cart_set.all()
        total = sum([item.get_total for item in cart])
        return total

    @property
    def get_cart_items(self):
        """
        Return total of items inside the cart
        """
        cart = self.cart_set.all()
        total = sum([item.quantity for item in cart])
        return total


class ShippingOption(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        """
        If there's no image, show nothing
        """
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    shipping_option = models.ForeignKey(ShippingOption, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Product: {self.product} - Order Number: {self.order} - Shipping Option: {self.shipping_option} - Quantity: {self.quantity}"

    @property
    def get_total(self):
        """
        Return total value inside the cart
        """
        total = self.product.price * self.quantity
        return total


class Checkout(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    shipping_option = models.ForeignKey(ShippingOption, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Checkout {self.order}"
