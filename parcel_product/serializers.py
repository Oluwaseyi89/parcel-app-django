from rest_framework import serializers
from .models import TempProduct, Product


class TempProductSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(max_length=80)
    vendor_phone = serializers.CharField(max_length=14)
    vendor_email = serializers.EmailField(max_length=70)
    vend_photo = serializers.CharField(max_length=200)
    prod_cat = serializers.CharField(max_length=25)
    prod_name = serializers.CharField(max_length=25)
    prod_model = serializers.CharField(max_length=40)
    prod_photo = serializers.ImageField()
    prod_price = serializers.IntegerField()
    prod_qty = serializers.IntegerField()
    prod_disc = serializers.IntegerField()
    prod_desc = serializers.CharField(max_length=200)
    img_base = serializers.CharField(max_length=200)
    upload_date = serializers.CharField(max_length=100)

    class Meta:
        model = TempProduct
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(max_length=80)
    vendor_phone = serializers.CharField(max_length=14)
    vendor_email = serializers.EmailField(max_length=70)
    vend_photo = serializers.CharField(max_length=200)
    prod_cat = serializers.CharField(max_length=25)
    prod_name = serializers.CharField(max_length=25)
    prod_model = serializers.CharField(max_length=40)
    prod_photo = serializers.CharField(max_length=200)
    prod_price = serializers.IntegerField()
    prod_qty = serializers.IntegerField()
    prod_disc = serializers.IntegerField()
    prod_desc = serializers.CharField(max_length=200)
    img_base = serializers.CharField(max_length=200)
    appr_officer = serializers.CharField(max_length=80)
    appr_date = serializers.CharField(max_length=100)
    updated_at = serializers.CharField(max_length=100)

    class Meta:
        model = Product
        fields = '__all__'


class ProductUpdateSerializer(serializers.ModelSerializer):
    prod_price = serializers.IntegerField()
    prod_qty = serializers.IntegerField()
    prod_disc = serializers.IntegerField()
    updated_at = serializers.CharField(max_length=100)

    class Meta:
        model = Product
        fields = ["prod_price", "prod_qty", "prod_disc", "updated_at"]



