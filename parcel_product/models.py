from django.db import models


# Create your models here.

class TempProduct(models.Model):
    vendor_name = models.CharField(max_length=80)
    vendor_phone = models.CharField(max_length=14)
    vendor_email = models.EmailField(max_length=70)
    vend_photo = models.CharField(max_length=200)
    prod_cat = models.CharField(max_length=25)
    prod_name = models.CharField(max_length=25)
    prod_model = models.CharField(max_length=40)
    prod_photo = models.ImageField(upload_to="product_images/")
    prod_price = models.IntegerField()
    prod_qty = models.IntegerField()
    prod_disc = models.IntegerField()
    prod_desc = models.TextField(max_length=500)
    img_base = models.CharField(max_length=200)
    upload_date = models.CharField(max_length=100, default="2022-04-23T12:25:32.355Z")

    def __str__(self):
        return self.prod_name


class Product(models.Model):
    vendor_name = models.CharField(max_length=80)
    vendor_phone = models.CharField(max_length=14)
    vendor_email = models.EmailField(max_length=70)
    vend_photo = models.CharField(max_length=200)
    prod_cat = models.CharField(max_length=25)
    prod_name = models.CharField(max_length=25)
    prod_model = models.CharField(max_length=40)
    prod_photo = models.CharField(max_length=200)
    prod_price = models.IntegerField()
    prod_qty = models.IntegerField()
    prod_disc = models.IntegerField()
    prod_desc = models.TextField(max_length=500)
    img_base = models.CharField(max_length=200)
    appr_officer = models.CharField(max_length=80)
    appr_date = models.CharField(max_length=100, default="2022-04-23T12:25:32.355Z")
    updated_at = models.CharField(max_length=100, default="2022-04-23T12:25:32.355Z")

    def __str__(self):
        return self.prod_name

