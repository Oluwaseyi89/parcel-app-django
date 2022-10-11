from django.db import models


# from django.contrib.gis.db import models

# Create your models here.

class DispatchDetail(models.Model):
    order_id = models.CharField(max_length=25)
    customer_id = models.CharField(max_length=25)
    customer_name = models.CharField(max_length=75)
    address = models.CharField(max_length=120)
    email = models.CharField(max_length=75)
    phone_no = models.CharField(max_length=14)
    is_customer = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    is_received = models.BooleanField(default=False)
    shipping_method = models.CharField(max_length=25)
    total_items = models.IntegerField()
    total_price = models.IntegerField()
    zip_code = models.CharField(max_length=25)
    handled_dispatch = models.BooleanField(default=False)
    courier_id = models.CharField(default="000", max_length=25)
    courier_email = models.CharField(default="000", max_length=25)
    courier_phone = models.CharField(default="000", max_length=25)
    courier_name = models.CharField(default="000", max_length=25)
    created_at = models.CharField(default="2022-04-23T12:25:32.355Z", max_length=100)
    updated_at = models.CharField(default="2022-04-23T12:25:32.355Z", max_length=100)

    def __str__(self):
        return self.customer_name


class DispatchedProduct(models.Model):
    order_id = models.CharField(max_length=25)
    product_id = models.CharField(max_length=25)
    product_name = models.CharField(max_length=75)
    prod_photo = models.CharField(max_length=200)
    prod_model = models.CharField(max_length=75)
    prod_price = models.IntegerField()
    quantity = models.IntegerField()
    total_amount = models.IntegerField()
    is_supply_ready = models.BooleanField(default=False)
    is_supply_received = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    is_received = models.BooleanField(default=False)
    vendor_email = models.CharField(max_length=75)
    vendor_phone = models.CharField(max_length=14)
    vendor_name = models.CharField(max_length=75)
    vendor_address = models.CharField(max_length=120)
    created_at = models.CharField(default="2022-04-23T12:25:32.355Z", max_length=100)
    updated_at = models.CharField(default="2022-04-23T12:25:32.355Z", max_length=100)

    def __str__(self):
        return self.product_name



