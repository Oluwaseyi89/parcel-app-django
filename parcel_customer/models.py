from django.db import models


# Create your models here.

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    phone_no = models.CharField(max_length=14)
    email = models.EmailField(max_length=70)
    password = models.CharField(max_length=200)
    reg_date = models.CharField(max_length=100)
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name


class AnonymousCustomer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    phone_no = models.CharField(max_length=14)
    email = models.EmailField(max_length=70)
    reg_date = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name


class CartSession(models.Model):
    customer_id = models.IntegerField()
    customer_name = models.CharField(max_length=100)
    total_items = models.IntegerField()
    total_price = models.IntegerField()
    ShippingChoices = models.TextChoices('ShippingMethod', 'Pick_up Delivery')
    shipping_method = models.CharField(blank=False, default='Pick up', choices=ShippingChoices.choices, max_length=25)
    zip_code = models.CharField(default='8000000', max_length=30)
    is_customer = models.BooleanField(default=False)
    created_at = models.CharField(max_length=100)
    updated_at = models.CharField(max_length=100)

    def __str__(self):
        return self.customer_name


class CartDetail(models.Model):
    session_id = models.IntegerField()
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    is_customer = models.BooleanField(default=False)
    created_at = models.CharField(max_length=100)
    updated_at = models.CharField(max_length=100)

    def __str__(self):
        return self.product_name
