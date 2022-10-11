from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import Customer, CartSession, AnonymousCustomer, CartDetail


class CustomerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    country = serializers.CharField(max_length=50)
    state = serializers.CharField(max_length=50)
    street = serializers.CharField(max_length=50)
    phone_no = serializers.CharField(max_length=14)
    email = serializers.EmailField(max_length=70)
    password = serializers.CharField(max_length=200)
    reg_date = serializers.CharField(max_length=100)
    is_email_verified = serializers.BooleanField()

    @staticmethod
    def validate_password(password: str) -> str:
        return make_password(password)

    class Meta:
        model = Customer
        fields = '__all__'


class CustomerLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=70)
    password = serializers.CharField(max_length=200)

    class Meta:
        model = Customer
        fields = ['email', 'password']


class CustomerResetSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=70)

    class Meta:
        model = Customer
        fields = ['email']


class CustomerSaveResetSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=70)
    password = serializers.CharField(max_length=200)

    @staticmethod
    def validate_password(password: str) -> str:
        return make_password(password)

    class Meta:
        model = Customer
        fields = ['email', 'password']


class CartSessionSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField()
    customer_name = serializers.CharField(max_length=100)
    total_items = serializers.IntegerField()
    total_price = serializers.IntegerField()
    shipping_method = serializers.CharField(max_length=25)
    zip_code = serializers.CharField(max_length=30)
    is_customer = serializers.BooleanField()
    created_at = serializers.CharField(max_length=100)
    updated_at = serializers.CharField(max_length=100)

    class Meta:
        model = CartSession
        fields = '__all__'


class CartDetailSerializer(serializers.ModelSerializer):
    session_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    product_name = serializers.CharField(max_length=100)
    quantity = serializers.IntegerField()
    is_customer = serializers.BooleanField()
    created_at = serializers.CharField(max_length=100)
    updated_at = serializers.CharField(max_length=100)

    class Meta:
        model = CartDetail
        fields = '__all__'


class AnonymousCustomerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    country = serializers.CharField(max_length=50)
    state = serializers.CharField(max_length=50)
    street = serializers.CharField(max_length=50)
    phone_no = serializers.CharField(max_length=14)
    email = serializers.EmailField(max_length=70)
    reg_date = serializers.CharField(max_length=100)

    class Meta:
        model = AnonymousCustomer
        fields = '__all__'
