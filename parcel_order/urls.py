from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import order, OrderSaveViews, OrderUpdateViews, OrderItemSaveViews, OrderItemUpdateViews, \
    GetOrderViews, DelOrderViews, PaymentDetailViews, PaymentDetailUpdateViews, GetOrderByIdViews, GetReadyOrdersViews, \
    GetDispatchableOrderItemsViews, UpdateOrderDispatchedViews, OrderUpdatePutViews, OrderItemSavePutViews, OrderItemUpdatePutViews, \
    PaymentDetailUpdatePutViews, UpdateOrderDispatchedMobileViews

urlpatterns = [
    path('order/', order, name="order"),
    path('order_update/<str:customer_name>/', csrf_exempt(OrderUpdateViews.as_view()), name="order_update"),
    path('order_update_mobile/<str:customer_name>/', csrf_exempt(OrderUpdatePutViews.as_view()), name="order_update"),
    path('order_save/<str:customer_name>/', OrderSaveViews.as_view(), name="order_save"),
    path('order_item_save/<str:order_id>/<str:product_id>/', csrf_exempt(OrderItemSaveViews.as_view()),
         name="order_item_save"),
    path('order_item_save_mobile/<str:order_id>/<str:product_id>/', csrf_exempt(OrderItemSavePutViews.as_view()),
         name="order_item_save_mobile"),
    path('order_item_update/<int:order_id>/<int:product_id>/', csrf_exempt(OrderItemUpdateViews.as_view()),
         name="order_item_update"),
    path('order_item_update_mobile/<int:order_id>/<int:product_id>/', csrf_exempt(OrderItemUpdatePutViews.as_view()),
         name="order_item_update_mobile"),
    path('get_order/<str:customer_name>/', GetOrderViews.as_view(), name="get_order"),
    path('get_order_id/<int:order_id>/', GetOrderByIdViews.as_view(), name="get_order_id"),
    path('del_order/<int:order_id>/', DelOrderViews.as_view(), name="del_order"),
    path('payment_save/<int:order_id>/', csrf_exempt(PaymentDetailViews.as_view()), name="payment_save"),
    path('payment_update/<int:order_id>/', csrf_exempt(PaymentDetailUpdateViews.as_view()), name="payment_update"),
    path('payment_update_mobile/<int:order_id>/', csrf_exempt(PaymentDetailUpdatePutViews.as_view()), name="payment_update"),
    path('update_order_dispatched/<int:order_id>/', UpdateOrderDispatchedViews.as_view(),
         name="update_order_dispatched"),
    path('update_order_dispatched_mobile/<int:order_id>/', csrf_exempt(UpdateOrderDispatchedMobileViews.as_view()),
         name="update_order_dispatched_mobile"),
    path('get_ready_orders/', GetReadyOrdersViews.as_view(), name="get_ready_orders"),
    path('get_dispatchable_items/<int:order_id>/', GetDispatchableOrderItemsViews.as_view(), name="get_dispatchable_items"),
    # path('base/', base, name="base"),
]
