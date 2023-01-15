import json
from django.core.mail import EmailMessage
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import MultiPartParser
import datetime

from .forms import MeasurementModelForm
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium
from .models import Staff, TempVendor, TempCourier, Vendor, Courier, VendorBankDetail, CourierBankDetail, \
    CustomerComplaint
from .serializers import TempVendorSerializer, TempCourierSerializer, VendorSerializer, CourierSerializer, \
    VendorLoginSerializer, CourierLoginSerializer, VendorResetSerializer, VendorSaveResetSerializer, \
    CourierResetSerializer, CourierSaveResetSerializer, VendorBankDetailSerializer, CourierBankDetailSerializer, \
    CustomerComplaintSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .utils import get_ip_address, get_geo, get_zoom, get_center_coords
# from django.contrib.auth.models import User
# from ..parcel_app.celery import add

import time


# Create your views here.

def home(request):
    return render(request, "parcel_backends\\parcel_admin.html")


def base(request):
    return render(request, "parcel_backends\\base.html")


def super_admin(request, *args, **kwargs):
    if request.method == 'POST':
        form_input = request.POST
        super_email = form_input['email']
        super_password = form_input['password']
        if super_password == "11jan2001" and super_email == "isenewoephr2012@gmail.com":
            return render(request, "parcel_backends\\staff.html")
        else:
            error_mess = {
                "mess": "Wrong Email or Password Entered!"
            }
            return render(request, "parcel_backends\\parcel_admin.html", error_mess)


def reg_staff(request):
    if request.method == 'POST':
        form_input = request.POST
        new_password = make_password(form_input['password'])
        first_name = form_input['first_name']
        last_name = form_input['last_name']
        phone = form_input['phone']
        # photo_name = form_input['photo']
        photo = request.FILES['photo']
        email = form_input['email']
        retyped_password = form_input['retype_password']
        # print(photo_name)
        if (len(first_name) == 0 or len(last_name) == 0 or len(phone) == 0 or len(email) == 0
                or len(retyped_password) == 0 or len(form_input['password']) == 0
                or retyped_password != form_input['password'] or len(photo) == 0):
            return render(request, "parcel_backends\\staff.html",
                          {"blank": "Fill the Missing Values and Match Password!"})
        else:
            try:
                pot_staff = Staff.objects.get(email=form_input['email'])
                if pot_staff is not None:
                    return render(request, "parcel_backends\\staff.html", {"exists": "Staff Already Exists"})
            except Staff.DoesNotExist:
                new_staff = Staff(first_name=first_name, last_name=last_name, phone=phone,
                                  email=email, password=new_password, photo=photo)
                new_staff.save()
                upload = request.FILES['photo']
                fss = FileSystemStorage()
                file = fss.save(upload.name, upload)
                file_url = fss.url(file)
                print(file_url)
                reg_mess = {
                    "success": "Your Registration Was Successfull!",
                    "failure": "An Error Occured Saving Your Details!"
                }
                return render(request, "parcel_backends\\staff.html", reg_mess)


def staff_login(request):
    return render(request, "parcel_backends\\staff_login.html")


def desk_login(request):
    if request.method == 'POST':
        form_input = request.POST
        staff_email = form_input['email']
        staff_password = form_input['password']
        check_staff = None
        try:
            check_staff = Staff.objects.get(email=staff_email)
        except Staff.DoesNotExist:
            return render(request, "parcel_backends\\staff_login.html", {"not_exist": "Staff is Not Registered Yet!"})
        if not check_password(staff_password, check_staff.password):
            return render(request, "parcel_backends\\staff_login.html", {"bad_password": "Wrong Password Entered"})
        else:
            # staff_photo = f'"<img" + "src=" + "{check_staff.photo}" + "/>"'
            return render(request, "parcel_backends\\admin_desk.html", {"first_name": check_staff.first_name,
                                                                        "id": check_staff.id,
                                                                        "last_name": check_staff.last_name,
                                                                        "photo": check_staff.photo})


@csrf_exempt
def desk_login_external(request, email=None, password=None):
    if request.method == 'POST':
        if email == "" or password == "":
            return JsonResponse({"status": "error", "data": "Enter all Fields"}, safe=True)
        else:
            try:
                check_staff = Staff.objects.get(email=email)
                if check_staff is not None:
                    if check_password(password, check_staff.password):
                        staff_data = {
                            "first_name": check_staff.first_name,
                            "id": check_staff.id,
                            "last_name": check_staff.last_name,
                        }
                        return HttpResponse(json.dumps({"status": "success", "data": staff_data}))
                    else:
                        return JsonResponse({"status": "error", "data": "Wrong password"}, safe=True)
            except Staff.DoesNotExist:
                return JsonResponse({"status": "error", "data": "Staff does not exist"}, safe=True)


def staff_reg_page(request):
    return render(request, "parcel_backends\\staff.html")


def handle_uploaded_file(f):
    with open('static\\media\\vendor_images', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


# handle_uploaded_file(request.FILES['vend_photo'])

# upload = request.FILES['vend_photo']
#         fss = FileSystemStorage()
#         file = fss.save(upload.name, upload)
#         file_url = fss.url(file)


def email_msg_view(request):
    current_site = get_current_site(request)
    user = Vendor.objects.get(email='deextralucid@gmail.com')
    message = render_to_string('parcel_backends\\activate_email_vend.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user)
    })
    return render(request, "parcel_backends\\activate_email_vend.html", message)


class TempVendorViews(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):
        serializer = TempVendorSerializer(data=request.data)
        if serializer.is_valid():
            try:
                prosp_vend = TempVendor.objects.get(email=request.data['email'])
                if prosp_vend is not None:
                    return Response({"status": "error", "data": "Vendor Already Exists"})

            except TempVendor.DoesNotExist:
                upload = request.FILES['vend_photo']
                fss = FileSystemStorage()
                file = fss.save(upload.name, upload)
                file_url = fss.url(file)
                print(file_url)
                serializer.save()
                user = TempVendor.objects.get(email=request.data['email'])
                print(user.pk)
                user.reg_date = datetime.datetime.today()
                user.save()
                current_site = get_current_site(request)
                mail_subject = "Activate your account"
                message = render_to_string('parcel_backends\\activate_email_vend.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user)
                })
                to_email = user.email
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                detail = f"Congratulation {user.first_name}, " \
                         f"you have been registered. Check your mail to " \
                         f"activate your account while waiting for approval."
                return Response({"status": "success", "data": detail})
        else:
            print(serializer.errors)
            return Response({"status": "error", "data": "Enter valid data please."})


def activate_vendor(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = TempVendor.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, TempVendor.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_email_verified = True
        user.save()
        data = {
            "message": "Your account has been activated successfully"
        }
        return render(request, "parcel_backends\\activation_page.html", data)
    else:
        err_msg = {
            "message": "The used link is invalid"
        }
        return render(request, "parcel_backends\\activation_page.html", err_msg)


def activate_courier(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = TempCourier.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, TempCourier.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_email_verified = True
        user.save()
        data = {
            "message": "Your account has been activated successfully"
        }
        return render(request, "parcel_backends\\activation_page.html", data)
    else:
        err_msg = {
            "message": "The used link is invalid"
        }
        return render(request, "parcel_backends\\activation_page.html", err_msg)


class VendorViews(APIView):
    def post(self, request):
        ver_vend = TempVendor.objects.get(email=request.data['email'])
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            try:
                vend = Vendor.objects.get(email=request.data['email'])
                if vend is not None:
                    return Response({"status": "error", "data": "Vendor Already Approved"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except Vendor.DoesNotExist:
                if not ver_vend.is_email_verified:
                    return Response({"status": "error", "data": "Vendor's Email has not been verified"})
                else:
                    serializer.save()
                    return Response({"status": "success", "data": "Vendor Approved"}, status=status.HTTP_200_OK)


class DelTempVendorViews(APIView):
    def delete(self, request, id=None):
        item = get_object_or_404(TempVendor, id=id)
        item.delete()
        return Response({"status": "success", "data": "Vendor Deleted"})


# @csrf_exempt
# def del_temp_vend(request):
#     if request.method == 'DELETE':
#         item = request.data['email']
#         try:
#             temp_vend = TempVendor.objects.get(email=item)
#             if temp_vend is not None:
#                 temp_vend.delete()
#                 return Response({"status": "success", "data": "Vendor Deleted"})
#         except TempVendor.DoesNotExist:
#             return Response({"status": "error", "data": "Vendor already deleted"})


class TempCourierViews(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):
        serializer = TempCourierSerializer(data=request.data)
        if serializer.is_valid():
            try:
                prosp_cour = TempCourier.objects.get(email=request.data['email'])
                if prosp_cour is not None:
                    return Response({"status": "error", "data": "Courier Already Exists"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except TempCourier.DoesNotExist:
                upload = request.FILES['cour_photo']
                fss = FileSystemStorage()
                file = fss.save(upload.name, upload)
                file_url = fss.url(file)
                print(file_url)
                serializer.save()
                user = TempCourier.objects.get(email=request.data['email'])
                print(user.pk)
                user.reg_date = datetime.datetime.today()
                user.save()
                current_site = get_current_site(request)
                mail_subject = "Activate your account"
                message = render_to_string('parcel_backends\\activate_email_cour.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user)
                })
                to_email = user.email
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                detail = f"Congratulation {user.first_name}, " \
                         f"you have been registered. Check your mail to " \
                         f"activate your account while waiting for approval."
                return Response({"status": "success", "data": detail}, status=status.HTTP_200_OK)


class GetTempVendorViews(APIView):
    def get(self, request, id=None):
        p_vendors = TempVendor.objects.all()
        serializer = TempVendorSerializer(p_vendors, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class GetVendorViews(APIView):
    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class GetVendorByEmailViews(APIView):
    def get(self, request, email=None):
        vendor = Vendor.objects.get(email=email)
        serializer = VendorSerializer(vendor)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class GetTempCourierViews(APIView):
    def get(self, request, id=None):
        p_couriers = TempCourier.objects.all()
        serializer = TempCourierSerializer(p_couriers, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class GetCourierViews(APIView):
    def get(self, request, id=None):
        couriers = Courier.objects.all()
        serializer = CourierSerializer(couriers, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class CourierViews(APIView):
    def post(self, request):
        ver_cour = TempCourier.objects.get(email=request.data['email'])
        serializer = CourierSerializer(data=request.data)
        if serializer.is_valid():
            try:
                cour = Courier.objects.get(email=request.data['email'])
                if cour is not None:
                    return Response({"status": "error", "data": "Courier Already Approved"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except Courier.DoesNotExist:
                if not ver_cour.is_email_verified:
                    return Response({"status": "error", "data": "Courier's Email has not been verified"})
                else:
                    serializer.save()
                    return Response({"status": "success", "data": "Courier Approved"}, status=status.HTTP_200_OK)


class DelTempCourierViews(APIView):
    def delete(self, request, id=None):
        item = get_object_or_404(TempCourier, id=id)
        item.delete()
        return Response({"status": "success", "data": "Courier Deleted"})


class VendorLoginViews(APIView):
    def post(self, request):
        serializer = VendorLoginSerializer(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            # print(serializer.errors)
            try:
                vendor = Vendor.objects.get(email=request.data['email'])
                if vendor is not None:
                    access = check_password(request.data['password'], vendor.password)
                    if access is True:
                        acc_vendor = {
                            "first_name": vendor.first_name,
                            "last_name": vendor.last_name,
                            "vend_photo": vendor.vend_photo,
                            "email": vendor.email,
                            "phone_no": vendor.phone_no,
                            "bus_category": vendor.bus_category
                        }
                        return Response({"status": "success", "data": acc_vendor})
                    else:
                        return Response(
                            {"status": "password-error", "data": "Wrong Password Supplied. Reset your password then."})
            except Vendor.DoesNotExist:
                try:
                    ver_vend = TempVendor.objects.get(email=request.data['email'])
                    if ver_vend is not None:
                        if ver_vend.is_email_verified is False:
                            return Response({"status": "error", "data": "You are yet to activate your account, check "
                                                                        "your "
                                                                        "mail to do so."})
                        else:
                            return Response({"status": "error", "data": "Your are yet to be approved."})
                except TempVendor.DoesNotExist:
                    return Response({"status": "error", "data": "Vendor does not exist, register please."})


class VendorResetViews(APIView):
    def post(self, request):
        serializer = VendorResetSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = Vendor.objects.get(email=request.data['email'])
                if user is not None:
                    current_site = get_current_site(request)
                    mail_subject = "Password Reset Link"
                    message = render_to_string('parcel_backends\\vendor_reset.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user)
                    })
                    to_email = user.email
                    email = EmailMessage(mail_subject, message, to=[to_email])
                    email.send()
                    detail = f"Dear {user.first_name}, " \
                             f"a password reset link has been sent to your mail. " \
                             f"Visit your mail to reset your password."
                    return Response({"status": "success", "data": detail}, status=status.HTTP_200_OK)
            except Vendor.DoesNotExist:
                return Response({"status": "error", "data": "E-Mail does not exist"})


def vendor_reset(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Vendor.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Vendor.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        data = {
            "message": "Reset Your Password",
            "type": "vendor",
            "permit": "true",
            "user": user.email
        }
        return render(request, "parcel_backends\\password_reset_page.html", data)
    else:
        err_msg = {
            "message": "The link has expired",
            "permit": "false"
        }
        return render(request, "parcel_backends\\password_reset_page.html", err_msg)


class VendorSaveResetViews(APIView):
    def post(self, request):
        serializer = VendorSaveResetSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = Vendor.objects.get(email=request.data['email'])
                if user is not None:
                    user.password = make_password(request.data['password'])
                    user.save()
                    data = "Your password has been reset successfully"
                    return Response({"status": "success", "data": data})
            except Vendor.DoesNotExist:
                return Response({"status": "error", "data": "User does not exist"})


class CourierLoginViews(APIView):
    def post(self, request):
        serializer = CourierLoginSerializer(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            # print(serializer.errors)
            try:
                courier = Courier.objects.get(email=request.data['email'])
                if courier is not None:
                    access = check_password(request.data['password'], courier.password)
                    if access is True:
                        acc_courier = {
                            "id": courier.id,
                            "first_name": courier.first_name,
                            "last_name": courier.last_name,
                            "cour_photo": courier.cour_photo,
                            "email": courier.email,
                            "phone_no": courier.phone_no
                        }
                        return Response({"status": "success", "data": acc_courier})
                    else:
                        return Response(
                            {"status": "password-error", "data": "Wrong Password Supplied. Reset your password then."})
            except Courier.DoesNotExist:
                try:
                    ver_cour = TempCourier.objects.get(email=request.data['email'])
                    if ver_cour is not None:
                        if ver_cour.is_email_verified is False:
                            return Response({"status": "error", "data": "You are yet to activate your account, check "
                                                                        "your "
                                                                        "mail to do so."})
                        else:
                            return Response({"status": "error", "data": "Your are yet to be approved."})
                except TempCourier.DoesNotExist:
                    return Response({"status": "error", "data": "Courier does not exist, register please."})


class CourierResetViews(APIView):
    def post(self, request):
        serializer = CourierResetSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = Courier.objects.get(email=request.data['email'])
                if user is not None:
                    current_site = get_current_site(request)
                    mail_subject = "Password Reset Link"
                    message = render_to_string('parcel_backends\\courier_reset.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user)
                    })
                    to_email = user.email
                    email = EmailMessage(mail_subject, message, to=[to_email])
                    email.send()
                    detail = f"Dear {user.first_name}, " \
                             f"a password reset link has been sent to your mail. " \
                             f"Visit your mail to reset your password."
                    return Response({"status": "success", "data": detail}, status=status.HTTP_200_OK)
            except Courier.DoesNotExist:
                return Response({"status": "error", "data": "E-Mail does not exist"})


def courier_reset(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Courier.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Courier.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        data = {
            "message": "Reset Your Password",
            "type": "courier",
            "permit": "true",
            "user": user.email
        }
        return render(request, "parcel_backends\\password_reset_page.html", data)
    else:
        err_msg = {
            "message": "The link has expired",
            "permit": "false"
        }
        return render(request, "parcel_backends\\password_reset_page.html", err_msg)


class CourierSaveResetViews(APIView):
    def post(self, request):
        serializer = CourierSaveResetSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = Courier.objects.get(email=request.data['email'])
                if user is not None:
                    user.password = make_password(request.data['password'])
                    user.save()
                    data = "Your password has been reset successfully"
                    return Response({"status": "success", "data": data})
            except Courier.DoesNotExist:
                return Response({"status": "error", "data": "User does not exist"})


class VendorBankDetailViews(APIView):
    def post(self, request):
        serializer = VendorBankDetailSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = VendorBankDetail.objects.get(vendor_email=request.data['vendor_email'])
                if user is not None:
                    return Response({"status": "error", "data": "Account details already uploaded, update instead."})
            except VendorBankDetail.DoesNotExist:
                serializer.save()
                return Response({"status": "success", "data": "Account details saved."})
        else:
            return Response({"status": "error", "data": "Enter valid data please."})


class GetDistinctVendorBankViews(APIView):
    def get(self, request, vendor_email=None):
        try:
            dist_vend_bank = VendorBankDetail.objects.get(vendor_email=vendor_email)
            serializer = VendorBankDetailSerializer(dist_vend_bank)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except VendorBankDetail.DoesNotExist:
            return Response({"status": "error", "data": "You have no bank details yet"},
                            status=status.HTTP_400_BAD_REQUEST)


class CourierBankDetailViews(APIView):
    def post(self, request):
        serializer = CourierBankDetailSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = CourierBankDetail.objects.get(courier_email=request.data['courier_email'])
                if user is not None:
                    return Response({"status": "error", "data": "Account details already uploaded, update instead."})
            except CourierBankDetail.DoesNotExist:
                serializer.save()
                return Response({"status": "success", "data": "Account details saved."})
        else:
            return Response({"status": "error", "data": "Enter valid data please."})


class VendorBankUpdateViews(APIView):
    def patch(self, request, vendor_email=None):
        try:
            item = VendorBankDetail.objects.get(vendor_email=vendor_email)
            serializer = VendorBankDetailSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "data": "Account details updated."})
            else:
                return Response({"status": "error", "data": "Enter valid data please."})
        except VendorBankDetail.DoesNotExist:
            return Response({"status": "error", "data": "Account not found, save one."})


class CourierBankUpdateViews(APIView):
    def patch(self, request, courier_email=None):
        try:
            item = CourierBankDetail.objects.get(courier_email=courier_email)
            serializer = VendorBankDetailSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "data": "Account details updated."})
            else:
                return Response({"status": "error", "data": "Enter valid data please."})
        except CourierBankDetail.DoesNotExist:
            return Response({"status": "error", "data": "Account not found, save one."})


class CustomerComplaintFormViews(APIView):
    def post(self, request):
        serializer = CustomerComplaintSerializer(data=request.data)
        if serializer.is_valid():
            try:
                subject = CustomerComplaint.objects.get(complaint_subject=request.data['complaint_subject'],
                                                        customer_email=request.data['customer_email'])
                if subject is not None:
                    return Response({"status": "error", "data": "Complaint already registered"})
            except CustomerComplaint.DoesNotExist:
                serializer.save()
                return Response({"status": "success", "data": "Your complaint has been registered"})
        else:
            print(serializer.errors)
            return Response({"status": "error", "data": "Enter valid data please."})


class CustomerComplaintUpdateViews(APIView):
    def patch(self, request, complaint_id=None):
        try:
            complaint = CustomerComplaint.objects.get(id=complaint_id)
            serializer = CustomerComplaintSerializer(complaint, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "data": "Complaint Updated."})
            else:
                return Response({"status": "error", "data": "Enter valid data please."})
        except CustomerComplaint.DoesNotExist:
            return Response({"status": "error", "data": "Complaint was never registered."})


class GetDistinctCustomerComplaintViews(APIView):
    def get(self, request, customer_email=None):
        try:
            dist_cus_complaint = CustomerComplaint.objects.filter(customer_email=customer_email)
            serializer = CustomerComplaintSerializer(dist_cus_complaint, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except CustomerComplaint.DoesNotExist:
            return Response({"status": "error", "data": "You are yet to upload any product"},
                            status=status.HTTP_400_BAD_REQUEST)


class GetAllCustomerComplaintsViews(APIView):
    def get(self, request):
        complaints = CustomerComplaint.objects.all()
        serializer = CustomerComplaintSerializer(complaints, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


def calculate_distance_view(request):
    distance = 0
    destination = None
    form = MeasurementModelForm(request.POST or None)
    geolocator = Nominatim(user_agent='parcel_backends')

    ip_ = get_ip_address(request)
    print(ip_)
    # ip = '197.210.78.32'
    ip = '197.210.76.118'
    # ip = '102.89.44.58'
    print(ip)
    country, city, lat, lon = get_geo(ip)
    location = geolocator.geocode(city)
    print(location)

    # location coordinates
    l_lat = lat
    l_lon = lon
    pointA = (l_lat, l_lon)
    print(pointA)

    # initial folium map
    m = folium.Map(width=800, height=500, location=get_center_coords(l_lat, l_lon), zoom_start=get_zoom(distance))

    # location marker
    folium.Marker([l_lat, l_lon], tooltip='click here for more', popup=city['city'],
                  icon=folium.Icon(color='purple')).add_to(m)

    if form.is_valid():
        instance = form.save(commit=False)
        destination_ = form.cleaned_data.get('destination')
        print(destination_)
        destination = geolocator.geocode(destination_)
        print(destination)

        # destination coordinates
        d_lat = destination.latitude
        d_lon = destination.longitude
        pointB = (d_lat, d_lon)
        print(pointB)

        # distance calculation
        distance = round(geodesic(pointA, pointB).km, 2)

        # folium map modification
        m = folium.Map(width=800, height=500, location=get_center_coords(l_lat, l_lon, d_lat, d_lon),
                       zoom_start=get_zoom(distance))

        # location marker
        folium.Marker([l_lat, l_lon], tooltip='click here for more', popup=city['city'],
                      icon=folium.Icon(color='purple')).add_to(m)
        # destination marker
        folium.Marker([d_lat, d_lon], tooltip='click here for more', popup=destination,
                      icon=folium.Icon(color='red')).add_to(m)

        line = folium.PolyLine(locations=[pointA, pointB], weight=5, color='blue')
        m.add_child(line)

        instance.location = 'Gonin-Gora Kaduna'
        instance.destination = destination
        instance.distance = distance
        instance.save()

    m = m._repr_html_()

    ctx = {
        "distance": distance,
        "destination": destination,
        "form": form,
        "map": m
    }
    return render(request, "parcel_backends\\geolocator.html", ctx)

# class GetStaffViews(APIView):
#     def get(self, request, id=None):
#         staff = Staff.objects.all()
#         serializer = StaffSerializer(staff, many=True)
#         return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

# def handle_uploaded_file(f):
#     with open('some/file/name.txt', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


# user = User.objects.create_user('emmanuel', 'emma@gmail.com', 'emma123')
# user.last_name = 'Alfred'
# user.save()
# #
# connection = mail.get_connection()
# connection.open()
# email = mail.EmailMessage('Testing Django Mailing', 'If you got this message it means django mailing works',
#                           'info@parcel.com', ['isenewoephr2012@gmail.com'], connection=connection)
# email.send()
# connection.close()
#
# task = add.delay(3, 5)
# print(task.status, task.result)
