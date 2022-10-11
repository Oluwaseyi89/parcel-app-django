from django.contrib import admin
from .models import DispatchDetail, DispatchedProduct

# Register your models here.

admin.site.register(DispatchDetail)
admin.site.register(DispatchedProduct)
