from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import customer, CustomerViews, activate_customer, CustomerLoginViews, CustomerResetViews, \
    CustomerSaveResetViews, CartSessionUpdateViews, CartSessionSaveViews, AnonymousCustomerViews, customer_reset, \
    CartDetailSaveViews, CartDetailUpdateViews, GetCartSessionViews, DelCartSessionViews, GetCustomerByIdViews, \
    GetAnonymousCustomerByIdViews

urlpatterns = [
    path('customer/', customer, name="customer"),
    path('reg_customer/', CustomerViews.as_view(), name="reg_customer"),
    path('reg_customer_mobile/', csrf_exempt(CustomerViews.as_view()), name="reg_customer_mobile"),
    path('activate_customer/<uidb64>/<token>', activate_customer, name="activate_customer"),
    path('customer_login/', CustomerLoginViews.as_view(), name="customer_login"),
    path('customer_login_mobile/', csrf_exempt(CustomerLoginViews.as_view()), name="customer_login_mobile"),
    path('customer_resetter/', CustomerResetViews.as_view(), name="customer_resetter"),
    path('cus_reset_save/', CustomerSaveResetViews.as_view(), name="cus_reset_save"),
    path('customer_reset/<uidb64>/<token>', customer_reset, name="customer_reset"),
    path('cart_update/<str:customer_name>/', CartSessionUpdateViews.as_view(), name="cart_update"),
    path('cart_save/<str:customer_name>/', CartSessionSaveViews.as_view(), name="cart_save"),
    path('prod_cart_save/<int:session_id>/<int:product_id>/', CartDetailSaveViews.as_view(), name="prod_cart_save"),
    path('prod_cart_update/<int:session_id>/<int:product_id>/', CartDetailUpdateViews.as_view(),
         name="prod_cart_update"),
    path('anonymous_save/', AnonymousCustomerViews.as_view(), name="anonymous_save"),
    path('get_cart/<str:customer_name>/', GetCartSessionViews.as_view(), name="get_cart"),
    path('del_cart/<int:session_id>/', DelCartSessionViews.as_view(), name="del_cart"),
    path('get_customer/<int:customer_id>/', GetCustomerByIdViews.as_view(), name="get_customer"),
    path('get_anon_customer/<int:customer_id>/', GetAnonymousCustomerByIdViews.as_view(), name="get_anon_customer"),
]
