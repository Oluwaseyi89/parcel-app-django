from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import TempVendor, TempCourier, Vendor, Courier, VendorBankDetail, CourierBankDetail, CustomerComplaint


class TempVendorSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    bus_country = serializers.CharField(max_length=50)
    bus_state = serializers.CharField(max_length=50)
    bus_street = serializers.CharField(max_length=50)
    bus_category = serializers.CharField(max_length=25)
    cac_reg_no = serializers.CharField(max_length=10)
    nin = serializers.CharField(max_length=11)
    phone_no = serializers.CharField(max_length=14)
    email = serializers.EmailField(max_length=70)
    vend_photo = serializers.ImageField()
    ven_policy = serializers.BooleanField()
    password = serializers.CharField(max_length=200)
    reg_date = serializers.CharField(max_length=100)
    is_email_verified = serializers.BooleanField()

    @staticmethod
    def validate_password(password: str) -> str:
        return make_password(password)

    class Meta:
        model = TempVendor
        fields = '__all__'


class VendorSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    bus_country = serializers.CharField(max_length=50)
    bus_state = serializers.CharField(max_length=50)
    bus_street = serializers.CharField(max_length=50)
    bus_category = serializers.CharField(max_length=25)
    cac_reg_no = serializers.CharField(max_length=10)
    nin = serializers.CharField(max_length=11)
    phone_no = serializers.CharField(max_length=14)
    email = serializers.EmailField(max_length=70)
    vend_photo = serializers.CharField(max_length=200)
    ven_policy = serializers.BooleanField()
    password = serializers.CharField(max_length=200)
    appr_officer = serializers.CharField(max_length=100)
    appr_date = serializers.CharField(max_length=100)
    is_email_verified = serializers.BooleanField()

    class Meta:
        model = Vendor
        fields = '__all__'


class TempCourierSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    bus_country = serializers.CharField(max_length=50)
    bus_state = serializers.CharField(max_length=50)
    bus_street = serializers.CharField(max_length=50)
    cac_reg_no = serializers.CharField(max_length=10)
    nin = serializers.CharField(max_length=11)
    phone_no = serializers.CharField(max_length=14)
    email = serializers.EmailField(max_length=70)
    cour_photo = serializers.ImageField()
    cour_policy = serializers.BooleanField()
    password = serializers.CharField(max_length=200)
    reg_date = serializers.CharField(max_length=100)
    is_email_verified = serializers.BooleanField()

    @staticmethod
    def validate_password(password: str) -> str:
        return make_password(password)

    class Meta:
        model = TempCourier
        fields = '__all__'


class CourierSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    bus_country = serializers.CharField(max_length=50)
    bus_state = serializers.CharField(max_length=50)
    bus_street = serializers.CharField(max_length=50)
    cac_reg_no = serializers.CharField(max_length=10)
    nin = serializers.CharField(max_length=11)
    phone_no = serializers.CharField(max_length=14)
    email = serializers.EmailField(max_length=70)
    cour_photo = serializers.CharField(max_length=200)
    cour_policy = serializers.BooleanField()
    password = serializers.CharField(max_length=200)
    appr_officer = serializers.CharField(max_length=100)
    appr_date = serializers.CharField(max_length=100)
    is_email_verified = serializers.BooleanField()

    class Meta:
        model = Courier
        fields = '__all__'


class VendorLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=70)
    password = serializers.CharField(max_length=200)

    class Meta:
        model = Vendor
        fields = ['email', 'password']


class CourierLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=70)
    password = serializers.CharField(max_length=200)

    class Meta:
        model = Courier
        fields = ['email', 'password']


class VendorResetSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=70)

    class Meta:
        model = Vendor
        fields = ['email']


class VendorSaveResetSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=70)
    password = serializers.CharField(max_length=200)

    @staticmethod
    def validate_password(password: str) -> str:
        return make_password(password)

    class Meta:
        model = Vendor
        fields = ['email', 'password']


class CourierResetSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=70)

    class Meta:
        model = Courier
        fields = ['email']


class CourierSaveResetSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=70)
    password = serializers.CharField(max_length=200)

    @staticmethod
    def validate_password(password: str) -> str:
        return make_password(password)

    class Meta:
        model = Courier
        fields = ['email', 'password']


class VendorBankDetailSerializer(serializers.ModelSerializer):
    bank_name = serializers.CharField(max_length=70)
    account_type = serializers.CharField(max_length=20)
    account_name = serializers.CharField(max_length=70)
    vendor_email = serializers.EmailField(max_length=70)
    account_no = serializers.CharField(max_length=15)
    added_at = serializers.CharField(max_length=50)
    updated_at = serializers.CharField(max_length=50)

    class Meta:
        model = VendorBankDetail
        fields = '__all__'


class CourierBankDetailSerializer(serializers.ModelSerializer):
    bank_name = serializers.CharField(max_length=70)
    account_type = serializers.CharField(max_length=20)
    account_name = serializers.CharField(max_length=70)
    courier_email = serializers.EmailField(max_length=70)
    account_no = serializers.CharField(max_length=15)
    added_at = serializers.CharField(max_length=50)
    updated_at = serializers.CharField(max_length=50)

    class Meta:
        model = CourierBankDetail
        fields = '__all__'


class CustomerComplaintSerializer(serializers.ModelSerializer):
    customer_email = serializers.CharField(max_length=70)
    complaint_subject = serializers.CharField(max_length=125)
    courier_involved = serializers.CharField(max_length=125)
    complaint_detail = serializers.CharField(max_length=1000)
    is_resolved = serializers.BooleanField()
    is_satisfied = serializers.BooleanField()

    class Meta:
        model = CustomerComplaint
        fields = '__all__'

