from django.db import models
# from django.contrib.gis.db import models


# Create your models here.

class OrderDetail(models.Model):
    customer_id = models.IntegerField()
    customer_name = models.CharField(max_length=100)
    total_items = models.IntegerField()
    total_price = models.IntegerField()
    ShippingChoices = models.TextChoices('ShippingMethod', 'Pick_up Delivery')
    shipping_method = models.CharField(blank=False, default='Pick up', choices=ShippingChoices.choices, max_length=25)
    shipping_fee = models.IntegerField(default=0)
    zip_code = models.CharField(default='8000000', max_length=30)
    payment_id = models.IntegerField(blank=False, default=0)
    is_customer = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    is_dispatched = models.BooleanField(default=False)
    created_at = models.CharField(max_length=100)
    updated_at = models.CharField(max_length=100)

    def __str__(self):
        return self.customer_name


class OrderItem(models.Model):
    order_id = models.IntegerField()
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    is_customer = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    created_at = models.CharField(max_length=100)
    updated_at = models.CharField(max_length=100)

    def __str__(self):
        return self.product_name


class CustomerPayment(models.Model):
    customer_id = models.IntegerField()
    customer_name = models.CharField(max_length=100)
    is_customer = models.BooleanField(default=False)
    PaymentChoices = models.TextChoices('PaymentType', 'Card Offline Bank')
    payment_type = models.CharField(blank=False, choices=PaymentChoices.choices, max_length=25)
    provider = models.CharField(max_length=50)
    account_no = models.CharField(max_length=15)
    expiry = models.CharField(max_length=50)

    def __str__(self):
        return self.customer_name


class PaymentDetail(models.Model):
    order_id = models.IntegerField()
    customer_id = models.IntegerField()
    customer_name = models.CharField(max_length=100)
    is_customer = models.BooleanField(default=False)
    amount = models.IntegerField()
    shipping_fee = models.IntegerField(default=0)
    grand_total_amount = models.IntegerField(default=0)
    ProviderChoices = models.TextChoices('ProviderChoice', 'Master_Card Verve_Card Visa_Card')
    provider = models.CharField(blank=False, choices=ProviderChoices.choices, max_length=50)
    PaymentChoices = models.TextChoices('PaymentType', 'Card_Payment Bank_Transfer Bank_Transfer_On_Delivery')
    payment_type = models.CharField(blank=False, choices=PaymentChoices.choices, max_length=25)
    StatusChoices = models.TextChoices('PaymentStatus', 'Successful Insufficient_Fund Failed Partial')
    status = models.CharField(blank=False, choices=StatusChoices.choices, max_length=50)
    reference = models.CharField(default="xxxxxxxx", max_length=25)
    created_at = models.CharField(max_length=100)
    updated_at = models.CharField(max_length=100)

    def __str__(self):
        return self.customer_name
