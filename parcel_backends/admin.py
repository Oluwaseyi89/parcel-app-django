from django.contrib import admin
from .models import Staff, TempVendor, TempCourier, Vendor, Courier, VendorBankDetail, CourierBankDetail, \
    Measurement

from django.apps import apps

# Register your models here.

admin.site.register(Staff)
admin.site.register(TempVendor)
admin.site.register(TempCourier)
admin.site.register(Vendor)
admin.site.register(Courier)
admin.site.register(VendorBankDetail)
admin.site.register(CourierBankDetail)
admin.site.register(Measurement)

# models = apps.get_models()
#
# for model in models:
#     try:
#         admin.site.register(model)
#     except admin.sites.AlreadyRegistered:
#         pass
