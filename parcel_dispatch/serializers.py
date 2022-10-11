from rest_framework import serializers

from .models import DispatchDetail, DispatchedProduct


class DispatchItemsSerializer(serializers.Serializer):
    dispatch_array = serializers.ListField


class DispatchDetailSerializer(serializers.ModelSerializer):
    order_id = serializers.CharField(max_length=25)
    customer_id = serializers.CharField(max_length=25)
    customer_name = serializers.CharField(max_length=75)
    address = serializers.CharField(max_length=120)
    email = serializers.CharField(max_length=75)
    phone_no = serializers.CharField(max_length=14)
    is_customer = serializers.BooleanField()
    is_delivered = serializers.BooleanField()
    is_received = serializers.BooleanField()
    shipping_method = serializers.CharField(max_length=25)
    total_items = serializers.IntegerField()
    total_price = serializers.IntegerField()
    zip_code = serializers.CharField(max_length=25)
    handled_dispatch = serializers.BooleanField()
    courier_id = serializers.CharField(max_length=25)
    courier_email = serializers.CharField(max_length=25)
    courier_phone = serializers.CharField(max_length=25)
    courier_name = serializers.CharField(max_length=25)
    created_at = serializers.CharField(max_length=100)
    updated_at = serializers.CharField(max_length=100)

    class Meta:
        model = DispatchDetail
        fields = '__all__'


class DispatchedProductSerializer(serializers.ModelSerializer):
    order_id = serializers.CharField(max_length=25)
    product_id = serializers.CharField(max_length=25)
    product_name = serializers.CharField(max_length=75)
    prod_photo = serializers.CharField(max_length=200)
    prod_model = serializers.CharField(max_length=75)
    prod_price = serializers.IntegerField()
    quantity = serializers.IntegerField()
    total_amount = serializers.IntegerField()
    is_supply_ready = serializers.BooleanField()
    is_supply_received = serializers.BooleanField()
    is_delivered = serializers.BooleanField()
    is_received = serializers.BooleanField()
    vendor_email = serializers.CharField(max_length=75)
    vendor_phone = serializers.CharField(max_length=14)
    vendor_name = serializers.CharField(max_length=75)
    vendor_address = serializers.CharField(max_length=120)
    created_at = serializers.CharField(max_length=100)
    updated_at = serializers.CharField(max_length=100)

    class Meta:
        model = DispatchedProduct
        fields = '__all__'



