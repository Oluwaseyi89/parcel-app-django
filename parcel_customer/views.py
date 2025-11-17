from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Customer, CartSession, AnonymousCustomer, CartDetail
from .serializers import CustomerSerializer, CustomerLoginSerializer, CustomerResetSerializer, \
    CustomerSaveResetSerializer, CartSessionSerializer, AnonymousCustomerSerializer, CartDetailSerializer
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site

# FIXED: Updated imports for Django 4.0+ compatibility
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from datetime import date, timedelta
import datetime


# Create your views here.


def customer(request):
    return render(request, "parcel_customer\\customer.html")


def make_date(front_end_date):
    f_date = str(front_end_date)
    f_sp1 = f_date.split('T')
    f_dt_ar = f_sp1[0]
    f_str = f_dt_ar.split('-')
    x = f_str
    y = [1, 2, 3]
    y[0] = int(x[0])
    y[1] = int(x[1])
    y[2] = int(x[2])
    z = y
    dt = date(z[0], z[1], z[2])
    return dt


def is_cart_expired(front_end_date):
    cur_date = date.today()
    exp_date = make_date(front_end_date) + timedelta(days=7)
    compare_date = exp_date < cur_date
    return compare_date


class CustomerViews(APIView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            try:
                pros_customer = Customer.objects.get(email=request.data['email'])
                if pros_customer is not None:
                    return Response({"status": "error", "data": "Customer Already Exists"})
            except Customer.DoesNotExist:
                serializer.save()
                user = Customer.objects.get(email=request.data['email'])
                print(user.pk)
                user.reg_date = datetime.datetime.today()
                user.save()
                current_site = get_current_site(request)
                mail_subject = "Activate your account"
                message = render_to_string('parcel_customer\\activate_email_customer.html', {
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
                         f"activate your account."
                return Response({"status": "success", "data": detail})
        else:
            print(serializer.errors)
            return Response({"status": "error", "data": "Enter Valid Data Please."})


def activate_customer(request, uidb64, token):
    try:
        # FIXED: Replaced force_text with force_str
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Customer.DoesNotExist):
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


class CustomerLoginViews(APIView):
    def post(self, request):
        serializer = CustomerLoginSerializer(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            try:
                cus = Customer.objects.get(email=request.data['email'])
                if cus is not None:
                    if not cus.is_email_verified:
                        return Response({"status": "error", "data": "Your account is yet to be activated, visit your "
                                                                    "mail to do so."})
                    else:
                        access = check_password(request.data['password'], cus.password)
                        if access is True:
                            acc_cus = {
                                "id": cus.id,
                                "first_name": cus.first_name,
                                "last_name": cus.last_name,
                                "email": cus.email,
                                "phone_no": cus.phone_no,
                                "country": cus.country,
                                "state": cus.state,
                                "street": cus.street
                            }
                            return Response({"status": "success", "data": acc_cus})
                        else:
                            return Response({"status": "password-error", "data": "Wrong Password Supplied. Reset your "
                                                                                 "password then."})
            except Customer.DoesNotExist:
                return Response({"status": "error", "data": "Customer does not exist, register please."})


class CustomerResetViews(APIView):
    def post(self, request):
        serializer = CustomerResetSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = Customer.objects.get(email=request.data['email'])
                if user is not None:
                    current_site = get_current_site(request)
                    mail_subject = "Password Reset Link"
                    message = render_to_string('parcel_customer\\customer_reset.html', {
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
            except Customer.DoesNotExist:
                return Response({"status": "error", "data": "E-Mail does not exist"})


def customer_reset(request, uidb64, token):
    try:
        # FIXED: Replaced force_text with force_str
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Customer.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        data = {
            "message": "Reset Your Password",
            "type": "customer",
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


class CustomerSaveResetViews(APIView):
    def post(self, request):
        serializer = CustomerSaveResetSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = Customer.objects.get(email=request.data['email'])
                if user is not None:
                    user.password = make_password(request.data['password'])
                    user.save()
                    data = "Your password has been reset successfully"
                    return Response({"status": "success", "data": data})
            except Customer.DoesNotExist:
                return Response({"status": "error", "data": "User does not exist"})


class CartSessionUpdateViews(APIView):
    def patch(self, request, customer_name=None):
        try:
            item = CartSession.objects.get(customer_name=customer_name)
            serializer = CartSessionSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                cart_create_date = item.created_at
                if not is_cart_expired(cart_create_date):
                    serializer.save()
                    saved_session = CartSession.objects.get(customer_name=customer_name)
                    session_id = saved_session.id
                    return Response({"status": "success", "data": session_id})
                else:
                    session_id = item.id
                    cart_detail = CartDetail.objects.filter(session_id=session_id)
                    for prod in cart_detail:
                        prod.delete()
                    item.delete()
                    return Response({"status": "error", "data": "Cart has expired"})
            else:
                return Response({"status": "invalid", "data": "Enter valid data please."})
        except CartSession.DoesNotExist:
            return Response({"status": "non-exist", "data": "Cart does not exist, create one"})


class CartSessionSaveViews(APIView):
    def post(self, request, customer_name=None):
        serializer = CartSessionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                cart = CartSession.objects.get(customer_name=customer_name)
                if cart is not None:
                    return Response({"status": "error", "data": "Cart already exists."})
            except CartSession.DoesNotExist:
                serializer.save()
                saved_session = CartSession.objects.get(customer_name=customer_name)
                session_id = saved_session.id
                return Response({"status": "success", "data": session_id})
        else:
            return Response({"status": "invalid", "data": "Enter valid data please."})


class AnonymousCustomerViews(APIView):
    def post(self, request):
        serializer = AnonymousCustomerSerializer(data=request.data)
        if serializer.is_valid():
            try:
                pros_customer = AnonymousCustomer.objects.get(email=request.data['email'])
                if pros_customer is not None:
                    customer_id = pros_customer.id
                    return Response({"status": "error", "data": customer_id},
                                    status=status.HTTP_400_BAD_REQUEST)
            except AnonymousCustomer.DoesNotExist:
                serializer.save()
                saved_customer = AnonymousCustomer.objects.get(email=request.data['email'])
                customer_id = saved_customer.id
                return Response({"status": "success", "data": customer_id}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "invalid", "data": "Enter valid data please."})


class CartDetailSaveViews(APIView):
    def post(self, request, session_id=None, product_id=None):
        serializer = CartDetailSerializer(data=request.data)
        if serializer.is_valid():
            try:
                cart = CartDetail.objects.get(session_id=session_id, product_id=product_id)
                print(cart)
                if cart is not None:
                    return Response({"status": "error", "data": "Product already exists"})
            except CartDetail.DoesNotExist:
                serializer.save()
                saved_prod = CartDetail.objects.get(product_id=product_id)
                returned_prod_id = saved_prod.id
                return Response({"status": "success", "data": "Cart Saved"})
        else:
            return Response({"status": "invalid", "data": "Enter valid data please."})


class CartDetailUpdateViews(APIView):
    def patch(self, request, session_id=None, product_id=None):
        try:
            item = CartDetail.objects.get(session_id=session_id, product_id=product_id)
            serializer = CartDetailSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                cart_create_date = item.created_at
                if not is_cart_expired(cart_create_date):
                    serializer.save()
                    saved_prod = CartDetail.objects.get(session_id=session_id, product_id=product_id)
                    detail_id = saved_prod.id
                    return Response({"status": "success", "data": "Cart Updated"})
                else:
                    return Response({"status": "expired", "data": "Cart has expired"})
            else:
                return Response({"status": "invalid", "data": "Enter valid data please."})
        except CartDetail.DoesNotExist:
            serializer = CartDetailSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "non-exist", "data": "New product Added"})


class GetCartSessionViews(APIView):
    def get(self, request, customer_name=None):
        try:
            dist_session = CartSession.objects.get(customer_name=customer_name)
            cart_create_date = dist_session.created_at
            if not is_cart_expired(cart_create_date):
                session_id = dist_session.id
                cart_details = CartDetail.objects.filter(session_id=session_id)
                serializer = CartDetailSerializer(cart_details, many=True)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                session_id = dist_session.id
                cart_detail = CartDetail.objects.filter(session_id=session_id)
                for prod in cart_detail:
                    prod.delete()
                dist_session.delete()
                return Response({"status": "error", "data": "Cart has expired"})
        except (CartSession.DoesNotExist, CartDetail.DoesNotExist):
            return Response({"status": "error", "data": "Cart Session does not exist"},
                            status=status.HTTP_400_BAD_REQUEST)


class DelCartSessionViews(APIView):
    def delete(self, request, session_id=None):
        cart_session = get_object_or_404(CartSession, id=session_id)
        sess_id = cart_session.id
        cart_detail = CartDetail.objects.filter(session_id=sess_id)
        for prod in cart_detail:
            prod.delete()
        cart_session.delete()
        return Response({"status": "success", "data": "Cart Items Deleted"})


class GetCustomerByIdViews(APIView):
    def get(self, request, customer_id=None):
        user = get_object_or_404(Customer, id=customer_id)
        serializer = CustomerSerializer(user)
        return Response({"status": "success", "data": serializer.data})


class GetAnonymousCustomerByIdViews(APIView):
    def get(self, request, customer_id=None):
        user = get_object_or_404(AnonymousCustomer, id=customer_id)
        serializer = AnonymousCustomerSerializer(user)
        return Response({"status": "success", "data": serializer.data})


















# from django.shortcuts import render
# from django.http import HttpResponse
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from .models import Customer, CartSession, AnonymousCustomer, CartDetail
# from .serializers import CustomerSerializer, CustomerLoginSerializer, CustomerResetSerializer, \
#     CustomerSaveResetSerializer, CartSessionSerializer, AnonymousCustomerSerializer, CartDetailSerializer
# from django.core.mail import EmailMessage
# from django.shortcuts import get_object_or_404
# from django.contrib.auth.hashers import make_password, check_password
# from django.template.loader import render_to_string
# from .tokens import account_activation_token
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_text, force_bytes
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from datetime import date, timedelta
# import datetime


# # Create your views here.


# def customer(request):
#     return render(request, "parcel_customer\\customer.html")


# def make_date(front_end_date):
#     f_date = str(front_end_date)
#     f_sp1 = f_date.split('T')
#     f_dt_ar = f_sp1[0]
#     f_str = f_dt_ar.split('-')
#     x = f_str
#     y = [1, 2, 3]
#     y[0] = int(x[0])
#     y[1] = int(x[1])
#     y[2] = int(x[2])
#     z = y
#     dt = date(z[0], z[1], z[2])
#     return dt


# def is_cart_expired(front_end_date):
#     cur_date = date.today()
#     exp_date = make_date(front_end_date) + timedelta(days=7)
#     compare_date = exp_date < cur_date
#     return compare_date


# class CustomerViews(APIView):
#     def post(self, request):
#         serializer = CustomerSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 pros_customer = Customer.objects.get(email=request.data['email'])
#                 if pros_customer is not None:
#                     return Response({"status": "error", "data": "Customer Already Exists"})
#             except Customer.DoesNotExist:
#                 serializer.save()
#                 user = Customer.objects.get(email=request.data['email'])
#                 print(user.pk)
#                 user.reg_date = datetime.datetime.today()
#                 user.save()
#                 current_site = get_current_site(request)
#                 mail_subject = "Activate your account"
#                 message = render_to_string('parcel_customer\\activate_email_customer.html', {
#                     'user': user,
#                     'domain': current_site.domain,
#                     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                     'token': account_activation_token.make_token(user)
#                 })
#                 to_email = user.email
#                 email = EmailMessage(mail_subject, message, to=[to_email])
#                 email.send()
#                 detail = f"Congratulation {user.first_name}, " \
#                          f"you have been registered. Check your mail to " \
#                          f"activate your account."
#                 return Response({"status": "success", "data": detail})
#         else:
#             print(serializer.errors)
#             return Response({"status": "error", "data": "Enter Valid Data Please."})


# def activate_customer(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = Customer.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, Customer.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_email_verified = True
#         user.save()
#         data = {
#             "message": "Your account has been activated successfully"
#         }
#         return render(request, "parcel_backends\\activation_page.html", data)
#     else:
#         err_msg = {
#             "message": "The used link is invalid"
#         }
#         return render(request, "parcel_backends\\activation_page.html", err_msg)


# class CustomerLoginViews(APIView):
#     def post(self, request):
#         serializer = CustomerLoginSerializer(data=request.data)
#         print(serializer.is_valid())
#         if serializer.is_valid():
#             try:
#                 cus = Customer.objects.get(email=request.data['email'])
#                 if cus is not None:
#                     if not cus.is_email_verified:
#                         return Response({"status": "error", "data": "Your account is yet to be activated, visit your "
#                                                                     "mail to do so."})
#                     else:
#                         access = check_password(request.data['password'], cus.password)
#                         if access is True:
#                             acc_cus = {
#                                 "id": cus.id,
#                                 "first_name": cus.first_name,
#                                 "last_name": cus.last_name,
#                                 "email": cus.email,
#                                 "phone_no": cus.phone_no,
#                                 "country": cus.country,
#                                 "state": cus.state,
#                                 "street": cus.street
#                             }
#                             return Response({"status": "success", "data": acc_cus})
#                         else:
#                             return Response({"status": "password-error", "data": "Wrong Password Supplied. Reset your "
#                                                                                  "password then."})
#             except Customer.DoesNotExist:
#                 return Response({"status": "error", "data": "Customer does not exist, register please."})


# class CustomerResetViews(APIView):
#     def post(self, request):
#         serializer = CustomerResetSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 user = Customer.objects.get(email=request.data['email'])
#                 if user is not None:
#                     current_site = get_current_site(request)
#                     mail_subject = "Password Reset Link"
#                     message = render_to_string('parcel_customer\\customer_reset.html', {
#                         'user': user,
#                         'domain': current_site.domain,
#                         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                         'token': account_activation_token.make_token(user)
#                     })
#                     to_email = user.email
#                     email = EmailMessage(mail_subject, message, to=[to_email])
#                     email.send()
#                     detail = f"Dear {user.first_name}, " \
#                              f"a password reset link has been sent to your mail. " \
#                              f"Visit your mail to reset your password."
#                     return Response({"status": "success", "data": detail}, status=status.HTTP_200_OK)
#             except Customer.DoesNotExist:
#                 return Response({"status": "error", "data": "E-Mail does not exist"})


# def customer_reset(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = Customer.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, Customer.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         data = {
#             "message": "Reset Your Password",
#             "type": "customer",
#             "permit": "true",
#             "user": user.email
#         }
#         return render(request, "parcel_backends\\password_reset_page.html", data)
#     else:
#         err_msg = {
#             "message": "The link has expired",
#             "permit": "false"
#         }
#         return render(request, "parcel_backends\\password_reset_page.html", err_msg)


# class CustomerSaveResetViews(APIView):
#     def post(self, request):
#         serializer = CustomerSaveResetSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 user = Customer.objects.get(email=request.data['email'])
#                 if user is not None:
#                     user.password = make_password(request.data['password'])
#                     user.save()
#                     data = "Your password has been reset successfully"
#                     return Response({"status": "success", "data": data})
#             except Customer.DoesNotExist:
#                 return Response({"status": "error", "data": "User does not exist"})


# class CartSessionUpdateViews(APIView):
#     def patch(self, request, customer_name=None):
#         try:
#             item = CartSession.objects.get(customer_name=customer_name)
#             serializer = CartSessionSerializer(item, data=request.data, partial=True)
#             if serializer.is_valid():
#                 cart_create_date = item.created_at
#                 if not is_cart_expired(cart_create_date):
#                     serializer.save()
#                     saved_session = CartSession.objects.get(customer_name=customer_name)
#                     session_id = saved_session.id
#                     return Response({"status": "success", "data": session_id})
#                 else:
#                     session_id = item.id
#                     cart_detail = CartDetail.objects.filter(session_id=session_id)
#                     for prod in cart_detail:
#                         prod.delete()
#                     item.delete()
#                     return Response({"status": "error", "data": "Cart has expired"})
#             else:
#                 return Response({"status": "invalid", "data": "Enter valid data please."})
#         except CartSession.DoesNotExist:
#             return Response({"status": "non-exist", "data": "Cart does not exist, create one"})


# class CartSessionSaveViews(APIView):
#     def post(self, request, customer_name=None):
#         serializer = CartSessionSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 cart = CartSession.objects.get(customer_name=customer_name)
#                 if cart is not None:
#                     return Response({"status": "error", "data": "Cart already exists."})
#             except CartSession.DoesNotExist:
#                 serializer.save()
#                 saved_session = CartSession.objects.get(customer_name=customer_name)
#                 session_id = saved_session.id
#                 return Response({"status": "success", "data": session_id})
#         else:
#             return Response({"status": "invalid", "data": "Enter valid data please."})


# class AnonymousCustomerViews(APIView):
#     def post(self, request):
#         serializer = AnonymousCustomerSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 pros_customer = AnonymousCustomer.objects.get(email=request.data['email'])
#                 if pros_customer is not None:
#                     customer_id = pros_customer.id
#                     return Response({"status": "error", "data": customer_id},
#                                     status=status.HTTP_400_BAD_REQUEST)
#             except AnonymousCustomer.DoesNotExist:
#                 serializer.save()
#                 saved_customer = AnonymousCustomer.objects.get(email=request.data['email'])
#                 customer_id = saved_customer.id
#                 return Response({"status": "success", "data": customer_id}, status=status.HTTP_200_OK)
#         else:
#             return Response({"status": "invalid", "data": "Enter valid data please."})


# class CartDetailSaveViews(APIView):
#     def post(self, request, session_id=None, product_id=None):
#         serializer = CartDetailSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 cart = CartDetail.objects.get(session_id=session_id, product_id=product_id)
#                 print(cart)
#                 if cart is not None:
#                     return Response({"status": "error", "data": "Product already exists"})
#             except CartDetail.DoesNotExist:
#                 serializer.save()
#                 saved_prod = CartDetail.objects.get(product_id=product_id)
#                 returned_prod_id = saved_prod.id
#                 return Response({"status": "success", "data": "Cart Saved"})
#         else:
#             return Response({"status": "invalid", "data": "Enter valid data please."})


# class CartDetailUpdateViews(APIView):
#     def patch(self, request, session_id=None, product_id=None):
#         try:
#             item = CartDetail.objects.get(session_id=session_id, product_id=product_id)
#             serializer = CartDetailSerializer(item, data=request.data, partial=True)
#             if serializer.is_valid():
#                 cart_create_date = item.created_at
#                 if not is_cart_expired(cart_create_date):
#                     serializer.save()
#                     saved_prod = CartDetail.objects.get(session_id=session_id, product_id=product_id)
#                     detail_id = saved_prod.id
#                     return Response({"status": "success", "data": "Cart Updated"})
#                 else:
#                     return Response({"status": "expired", "data": "Cart has expired"})
#             else:
#                 return Response({"status": "invalid", "data": "Enter valid data please."})
#         except CartDetail.DoesNotExist:
#             serializer = CartDetailSerializer(data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response({"status": "non-exist", "data": "New product Added"})


# class GetCartSessionViews(APIView):
#     def get(self, request, customer_name=None):
#         try:
#             dist_session = CartSession.objects.get(customer_name=customer_name)
#             cart_create_date = dist_session.created_at
#             if not is_cart_expired(cart_create_date):
#                 session_id = dist_session.id
#                 cart_details = CartDetail.objects.filter(session_id=session_id)
#                 serializer = CartDetailSerializer(cart_details, many=True)
#                 return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
#             else:
#                 session_id = dist_session.id
#                 cart_detail = CartDetail.objects.filter(session_id=session_id)
#                 for prod in cart_detail:
#                     prod.delete()
#                 dist_session.delete()
#                 return Response({"status": "error", "data": "Cart has expired"})
#         except (CartSession.DoesNotExist, CartDetail.DoesNotExist):
#             return Response({"status": "error", "data": "Cart Session does not exist"},
#                             status=status.HTTP_400_BAD_REQUEST)


# class DelCartSessionViews(APIView):
#     def delete(self, request, session_id=None):
#         cart_session = get_object_or_404(CartSession, id=session_id)
#         sess_id = cart_session.id
#         cart_detail = CartDetail.objects.filter(session_id=sess_id)
#         for prod in cart_detail:
#             prod.delete()
#         cart_session.delete()
#         return Response({"status": "success", "data": "Cart Items Deleted"})


# class GetCustomerByIdViews(APIView):
#     def get(self, request, customer_id=None):
#         user = get_object_or_404(Customer, id=customer_id)
#         serializer = CustomerSerializer(user)
#         return Response({"status": "success", "data": serializer.data})


# class GetAnonymousCustomerByIdViews(APIView):
#     def get(self, request, customer_id=None):
#         user = get_object_or_404(AnonymousCustomer, id=customer_id)
#         serializer = AnonymousCustomerSerializer(user)
#         return Response({"status": "success", "data": serializer.data})





