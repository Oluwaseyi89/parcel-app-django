from django.contrib import admin
from .models import TempProduct, Product
from django.apps import apps

# Register your models here.

admin.site.register(TempProduct)
admin.site.register(Product)
