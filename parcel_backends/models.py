import win32timezone
from django.db import models
from datetime import datetime
from django.utils import timezone


# Create your models here.

class Staff(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=14)
    email = models.EmailField(max_length=80)
    photo = models.ImageField(upload_to='staff-photo/')
    password = models.CharField(max_length=100)
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name


class TempVendor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    bus_country = models.CharField(max_length=50)
    bus_state = models.CharField(max_length=50)
    bus_street = models.CharField(max_length=50)
    BusCategories = models.TextChoices('BusCategory', 'Clothing Electronics Chemicals Educative_Materials Furniture '
                                                      'Kitchen_Utensils Plastics Spare_Parts General_Merchandise')
    bus_category = models.CharField(blank=True, choices=BusCategories.choices, max_length=25)
    cac_reg_no = models.CharField(max_length=10)
    nin = models.CharField(max_length=11, default='11111111111')
    phone_no = models.CharField(max_length=14)
    email = models.EmailField(max_length=70)
    vend_photo = models.ImageField(upload_to='vendor_images/')
    ven_policy = models.BooleanField()
    password = models.CharField(max_length=200)
    reg_date = models.CharField(max_length=100, default="2022-04-23T12:25:32.355Z")
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name


class Vendor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    bus_country = models.CharField(max_length=50)
    bus_state = models.CharField(max_length=50)
    bus_street = models.CharField(max_length=50)
    bus_category = models.CharField(max_length=25)
    cac_reg_no = models.CharField(max_length=10)
    nin = models.CharField(max_length=11, default='11111111111')
    phone_no = models.CharField(max_length=14)
    email = models.EmailField(max_length=70)
    vend_photo = models.CharField(max_length=200)
    ven_policy = models.BooleanField()
    password = models.CharField(max_length=200)
    appr_officer = models.CharField(max_length=100)
    appr_date = models.CharField(max_length=100, default="2022-04-23T12:25:32.355Z")
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name


class TempCourier(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    bus_country = models.CharField(max_length=50)
    bus_state = models.CharField(max_length=50)
    bus_street = models.CharField(max_length=50)
    cac_reg_no = models.CharField(max_length=10)
    nin = models.CharField(max_length=11, default='11111111111')
    phone_no = models.CharField(max_length=14)
    email = models.EmailField(max_length=70)
    cour_photo = models.ImageField(upload_to='courier_images/')
    cour_policy = models.BooleanField()
    password = models.CharField(max_length=200)
    reg_date = models.CharField(max_length=100, default="2022-04-23T12:25:32.355Z")
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name


class Courier(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    bus_country = models.CharField(max_length=50)
    bus_state = models.CharField(max_length=50)
    bus_street = models.CharField(max_length=50)
    cac_reg_no = models.CharField(max_length=10)
    nin = models.CharField(max_length=11, default='11111111111')
    phone_no = models.CharField(max_length=14)
    email = models.EmailField(max_length=70)
    cour_photo = models.CharField(max_length=200)
    cour_policy = models.BooleanField()
    password = models.CharField(max_length=200)
    appr_officer = models.CharField(max_length=100)
    appr_date = models.CharField(max_length=100, default="2022-04-23T12:25:32.355Z")
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name


class VendorBankDetail(models.Model):
    bank_name = models.CharField(max_length=70)
    AccountType = models.TextChoices('AccountType', 'Savings Current')
    account_type = models.CharField(blank=False, choices=AccountType.choices, max_length=20)
    account_name = models.CharField(max_length=70)
    vendor_email = models.EmailField(max_length=70)
    account_no = models.CharField(max_length=15)
    added_at = models.CharField(max_length=50)
    updated_at = models.CharField(max_length=50)

    def __str__(self):
        return self.account_name


class CourierBankDetail(models.Model):
    bank_name = models.CharField(max_length=70)
    AccountType = models.TextChoices('AccountType', 'Savings Current')
    account_type = models.CharField(blank=False, choices=AccountType.choices, max_length=20)
    account_name = models.CharField(max_length=70)
    courier_email = models.EmailField(max_length=70)
    account_no = models.CharField(max_length=15)
    added_at = models.CharField(max_length=50)
    updated_at = models.CharField(max_length=50)

    def __str__(self):
        return self.account_name


class CustomerComplaint(models.Model):
    customer_email = models.CharField(max_length=70)
    complaint_subject = models.CharField(max_length=125)
    courier_involved = models.CharField(max_length=125, default="Anonymous")
    complaint_detail = models.TextField(max_length=1000)
    is_resolved = models.BooleanField()
    is_satisfied = models.BooleanField()

    def __str__(self):
        return self.complaint_subject


class Measurement(models.Model):
    location = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Distance from {self.location} to {self.destination} is " \
               f"{self.distance} km"
