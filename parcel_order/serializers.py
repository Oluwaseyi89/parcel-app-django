from rest_framework import serializers
from .models import OrderDetail, OrderItem, PaymentDetail


class OrderDetailSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField()
    customer_name = serializers.CharField(max_length=100)
    total_items = serializers.IntegerField()
    total_price = serializers.IntegerField()
    shipping_method = serializers.CharField(max_length=25)
    shipping_fee = serializers.IntegerField()
    zip_code = serializers.CharField(max_length=30)
    payment_id = serializers.IntegerField()
    is_customer = serializers.BooleanField()
    is_completed = serializers.BooleanField()
    is_dispatched = serializers.BooleanField()
    created_at = serializers.CharField(max_length=100)
    updated_at = serializers.CharField(max_length=100)

    class Meta:
        model = OrderDetail
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    product_name = serializers.CharField(max_length=100)
    quantity = serializers.IntegerField()
    is_customer = serializers.BooleanField()
    is_completed = serializers.BooleanField()
    created_at = serializers.CharField(max_length=100)
    updated_at = serializers.CharField(max_length=100)

    class Meta:
        model = OrderItem
        fields = '__all__'


class PaymentDetailSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField()
    customer_id = serializers.IntegerField()
    customer_name = serializers.CharField(max_length=100)
    is_customer = serializers.BooleanField()
    amount = serializers.IntegerField()
    shipping_fee = serializers.IntegerField()
    grand_total_amount = serializers.IntegerField()
    provider = serializers.CharField(max_length=50)
    payment_type = serializers.CharField(max_length=25)
    status = serializers.CharField(max_length=50)
    reference = serializers.CharField(max_length=25)
    created_at = serializers.CharField(max_length=100)
    updated_at = serializers.CharField(max_length=100)

    class Meta:
        model = PaymentDetail
        fields = '__all__'
