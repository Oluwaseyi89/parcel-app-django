from django.contrib import admin
from .models import OrderItem, OrderDetail, PaymentDetail, CustomerPayment

# Register your models here.

admin.site.register(OrderDetail)
admin.site.register(OrderItem)
admin.site.register(PaymentDetail)
admin.site.register(CustomerPayment)
