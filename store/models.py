from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    email = models.EmailField(null=True, max_length=200)
    name = models.CharField(null=True, max_length=20)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=20, null=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(upload_to='images', null=True, default='images/avatar_hy6hxz.jpg')

    def __str__(self):
        return self.name

    @property
    def imageUrl(self):  # in the case that the url is empty
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=20, null=False)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderItem = self.orderitem_set.all()
        for i in orderItem:
            if not i.product.digital:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.getTotal for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=False)
    added_ordered = models.DateTimeField(auto_now_add=True)

    @property
    def getTotal(self):  # To get the cart total item
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=20, null=False)
    city = models.CharField(max_length=20, null=False)
    detailed_address = models.CharField(max_length=20, null=False)
    zip_code = models.CharField(max_length=20, null=False)

    def __str__(self):
        return self.address
