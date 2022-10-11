from django.contrib import admin
from .models import Customer, CartDetail, CartSession, AnonymousCustomer

# Register your models here.


admin.site.register(Customer)
admin.site.register(CartDetail)
admin.site.register(CartSession)
admin.site.register(AnonymousCustomer)
