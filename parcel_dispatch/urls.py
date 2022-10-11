from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import dispatch, get_products, get_ready_orders, SaveDispatchDetailViews, SaveDispatchedProductViews, \
    UpdateDispatchedProductViews, UpdateDispatchDetailViews, get_dispatches_views, update_supply_ready, \
    update_supply_received, UpdateDispatchedProductMobileViews, UpdateDispatchDetailMobileViews # GetReadyOrdersViews

urlpatterns = [
    path('dispatch/', dispatch, name="dispatch"),
    path('resend_prod/', get_products, name="resend_prod"),
    path('get_ready_orders/', get_ready_orders, name="get_ready_orders"),
    path('save_dispatch/<int:order_id>/', SaveDispatchDetailViews.as_view(), name="save_dispatch"),
    path('save_dispatched_product/<int:order_id>/<int:product_id>/', SaveDispatchedProductViews.as_view(),
         name="save_dispatched_product"),
    path('update_dispatch/<int:order_id>/', UpdateDispatchDetailViews.as_view(), name="update_dispatch"),
    path('update_dispatch_mobile/<int:order_id>/', csrf_exempt(UpdateDispatchDetailMobileViews.as_view()),
         name="update_dispatch_mobile"),
    path('update_dispatched_product/<int:order_id>/<int:product_id>/', UpdateDispatchedProductViews.as_view(),
         name="update_dispatched_product"),
    path('update_dispatched_product_mobile/<int:order_id>/<int:product_id>/',
         csrf_exempt(UpdateDispatchedProductMobileViews.as_view()), name="update_dispatched_product_mobile"),
    path('update_supplied_product/<int:order_id>/<int:product_id>/', update_supply_ready,
         name="update_dispatched_product"),
    path('update_received_product/<int:order_id>/<int:product_id>/', update_supply_received,
         name="update_received_product"),
    path('get_dispatch_from_db/', get_dispatches_views, name="get_dispatch_from_db"),
    # path('get_ready_orders_api/', GetReadyOrdersViews.as_view(), name="get_ready_orders_api"),
    # path('base/', base, name="base"),
]
