from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from .views import home, base, super_admin, reg_staff, staff_login, desk_login, staff_reg_page, \
    TempVendorViews, TempCourierViews, GetTempVendorViews, GetTempCourierViews, VendorViews, DelTempVendorViews, \
    CourierViews, DelTempCourierViews, GetCourierViews, GetVendorViews, VendorLoginViews, CourierLoginViews, email_msg_view,\
    activate_vendor, activate_courier, VendorResetViews, vendor_reset, VendorSaveResetViews, CourierResetViews, \
    CourierSaveResetViews, courier_reset, VendorBankDetailViews, VendorBankUpdateViews, GetVendorByEmailViews, \
    CourierBankDetailViews, CourierBankUpdateViews, calculate_distance_view, desk_login_external

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name="home"),
    path('base/', base, name="base"),
    path('super_admin/', super_admin, name="super_admin"),
    path('reg_staff/', reg_staff, name="reg_staff"),
    path('staff_login/', staff_login, name="staff_login"),
    path('desk_login/', desk_login, name="desk_login"),
    path('desk_login_ext/<str:email>/<str:password>/', desk_login_external, name="desk_login_ext"),
    path('staff_reg_page/', staff_reg_page, name="staff_reg_page"),
    path('update_vend_bank/<str:vendor_email>', VendorBankUpdateViews.as_view(), name="update_vend_bank"),
    path('update_cour_bank/<str:courier_email>', CourierBankUpdateViews.as_view(), name="update_cour_bank"),
    path('save_vend_bank/', VendorBankDetailViews.as_view(), name="save_vend_bank"),
    path('save_cour_bank/', CourierBankDetailViews.as_view(), name="save_cour_bank"),
    path('reg_temp_ven/', TempVendorViews.as_view(), name="reg_temp_ven"),
    path('reg_temp_ven_mobile/', csrf_exempt(TempVendorViews.as_view()), name="reg_temp_ven_mobile"),
    path('reg_temp_cour/', TempCourierViews.as_view(), name="reg_temp_cour"),
    path('reg_temp_cour_mobile/', csrf_exempt(TempCourierViews.as_view()), name="reg_temp_cour_mobile"),
    path('get_temp_ven/', GetTempVendorViews.as_view(), name="get_temp_ven"),
    path('get_temp_cour/', GetTempCourierViews.as_view(), name="get_temp_cour"),
    path('get_ven/', GetVendorViews.as_view(), name="get_ven"),
    path('get_ven_email/<str:email>/', GetVendorByEmailViews.as_view(), name="get_ven_email"),
    path('get_cour/', GetCourierViews.as_view(), name="get_cour"),
    path('appr_vendor/', VendorViews.as_view(), name="appr_vendor"),
    path('del_temp_vendor/<int:id>/', DelTempVendorViews.as_view(), name="del_temp_vendor"),
    path('appr_courier/', CourierViews.as_view(), name="appr_courier"),
    path('del_temp_courier/<int:id>/', DelTempCourierViews.as_view(), name="del_temp_courier"),
    path('vendor_login/', VendorLoginViews.as_view(), name="vendor_login"),
    path('vendor_login_mobile/', csrf_exempt(VendorLoginViews.as_view()), name="vendor_login_mobile"),
    path('courier_login/', CourierLoginViews.as_view(), name="courier_login"),
    path('courier_login_mobile/', csrf_exempt(CourierLoginViews.as_view()), name="courier_login_mobile"),
    path('vendor_resetter/', VendorResetViews.as_view(), name="vendor_resetter"),
    path('courier_resetter/', CourierResetViews.as_view(), name="courier_resetter"),
    path('ven_reset_save/', VendorSaveResetViews.as_view(), name="ven_reset_save"),
    path('cour_reset_save/', CourierSaveResetViews.as_view(), name="cour_reset_save"),
    path('email_msg/', email_msg_view, name="email_msg"),
    path('activate_vendor/<uidb64>/<token>', activate_vendor, name="activate_vendor"),
    path('activate_courier/<uidb64>/<token>', activate_courier, name="activate_courier"),
    path('vendor_reset/<uidb64>/<token>', vendor_reset, name="vendor_reset"),
    path('courier_reset/<uidb64>/<token>', courier_reset, name="courier_reset"),
    path('calculate_distance/', calculate_distance_view, name="calculate_distance"),
    # url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate,
    # name="activate"),
]
