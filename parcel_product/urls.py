from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import product, TempProductViews, GetTempProductViews, GetProductViews, ProductViews, \
    DelTempProductViews, GetDistinctVendorProductViews, ProductUpdateViews, DelProductViews, \
    GetDistinctVendTempProductViews, GetSingleProductViews
urlpatterns = [
    path('product/', product, name="product"),
    path('product_upload/', TempProductViews.as_view(), name="product_upload"),
    path('product_upload_mobile/', csrf_exempt(TempProductViews.as_view()), name="product_upload_mobile"),
    path('get_temp_prod/', GetTempProductViews.as_view(), name="get_temp_prod"),
    path('get_prod/', GetProductViews.as_view(), name="get_prod"),
    path('get_sing_prod/<int:id>/', GetSingleProductViews.as_view(), name="get_sing_prod"),
    path('appr_product/', ProductViews.as_view(), name="appr_product"),
    path('del_temp_product/<int:id>/', DelTempProductViews.as_view(), name="del_temp_product"),
    path('del_product/<int:id>/', DelProductViews.as_view(), name="del_product"),
    path('del_product_mobile/<int:id>/', csrf_exempt(DelProductViews.as_view()), name="del_product_mobile"),
    path('update_product/<int:id>/', ProductUpdateViews.as_view(), name="update_product"),
    path('update_product_mobile/<int:id>/', csrf_exempt(ProductUpdateViews.as_view()), name="update_product_mobile"),
    path('get_dist_ven_product/<str:vendor_email>/', GetDistinctVendorProductViews.as_view(),
         name="get_dist_ven_product"),
    path('get_dist_temp_product/<str:vendor_email>/', GetDistinctVendTempProductViews.as_view(),
         name="get_dist_temp_product"),
    # path('base/', base, name="base"),
]
