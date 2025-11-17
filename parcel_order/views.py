from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import OrderDetail, OrderItem, PaymentDetail
from .serializers import OrderDetailSerializer, OrderItemSerializer, PaymentDetailSerializer
from django.shortcuts import get_object_or_404
from datetime import date, timedelta
import datetime


def order(request):
    return render(request, "parcel_order\\order.html")


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


class OrderUpdateViews(APIView):
    def patch(self, request, customer_name=None):
        try:
            item = OrderDetail.objects.get(customer_name=customer_name, is_completed=False)
            serializer = OrderDetailSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                cart_create_date = item.created_at
                if not is_cart_expired(cart_create_date):
                    serializer.save()
                    saved_order = OrderDetail.objects.get(customer_name=customer_name, is_completed=False)
                    order_id = saved_order.id
                    if saved_order.shipping_method == 'Delivery':
                        saved_order.shipping_fee = 500
                        saved_order.save()
                    else:
                        saved_order.shipping_fee = 0
                        saved_order.save()
                    saved_order.updated_at = str(datetime.datetime.today()).replace(" ", "T")
                    saved_order.save()
                    return Response({"status": "success", "data": order_id})
                else:
                    order_id = item.id
                    order_items = OrderItem.objects.filter(order_id=order_id)
                    for prod in order_items:
                        prod.delete()
                    item.delete()
                    return Response({"status": "error", "data": "Order has expired"})
            else:
                return Response({"status": "invalid", "data": "Enter valid data please."})
        except OrderDetail.DoesNotExist:
            return Response({"status": "non-exist", "data": "Order does not exist, place one"})


class OrderUpdatePutViews(APIView):
    def put(self, request, customer_name=None):
        try:
            item = OrderDetail.objects.get(customer_name=customer_name, is_completed=False)
            serializer = OrderDetailSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                cart_create_date = item.created_at
                if not is_cart_expired(cart_create_date):
                    serializer.save()
                    saved_order = OrderDetail.objects.get(customer_name=customer_name, is_completed=False)
                    order_id = saved_order.id
                    if saved_order.shipping_method == 'Delivery':
                        saved_order.shipping_fee = 500
                        saved_order.save()
                    else:
                        saved_order.shipping_fee = 0
                        saved_order.save()
                    saved_order.updated_at = str(datetime.datetime.today()).replace(" ", "T")
                    saved_order.save()
                    return Response({"status": "success", "data": order_id})
                else:
                    order_id = item.id
                    order_items = OrderItem.objects.filter(order_id=order_id)
                    for prod in order_items:
                        prod.delete()
                    item.delete()
                    return Response({"status": "error", "data": "Order has expired"})
            else:
                return Response({"status": "invalid", "data": "Enter valid data please."})
        except OrderDetail.DoesNotExist:
            return Response({"status": "non-exist", "data": "Order does not exist, place one"})


class OrderSaveViews(APIView):
    def post(self, request, customer_name=None):
        serializer = OrderDetailSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            try:
                item = OrderDetail.objects.get(customer_name=customer_name, is_completed=False)
                if item is not None:
                    # for some in item:
                    #     if some.is_completed:
                    #         serializer.save()
                    #         saved_order = OrderDetail.objects.get(customer_name=customer_name, is_completed=False)
                    #         order_id = saved_order.id
                    #         if saved_order.shipping_method == 'Delivery':
                    #             saved_order.shipping_fee = 500
                    #             saved_order.save()
                    #         return Response({"status": "success", "data": order_id})
                    #     else:
                    return Response({"status": "error", "data": "Order already placed."})
            except OrderDetail.DoesNotExist:
                serializer.save()
                saved_order = OrderDetail.objects.get(customer_name=customer_name, is_completed=False)
                order_id = saved_order.id
                if saved_order.shipping_method == 'Delivery':
                    saved_order.shipping_fee = 500
                    saved_order.save()
                else:
                    saved_order.shipping_fee = 0
                    saved_order.save()
                saved_order.created_at = str(datetime.datetime.today()).replace(" ", "T")
                saved_order.updated_at = str(datetime.datetime.today()).replace(" ", "T")
                saved_order.save()
                return Response({"status": "success", "data": order_id})
        else:
            return Response({"status": "invalid", "data": "Enter valid data please."})


class OrderItemSaveViews(APIView):
    def patch(self, request, order_id=None, product_id=None):
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            try:
                item = OrderItem.objects.get(order_id=order_id, product_id=product_id, is_completed=False)
                print(item)
                if item is not None:
                    return Response({"status": "error", "data": "Product already exists"})
            except OrderItem.DoesNotExist:
                serializer.save()
                saved_item = OrderItem.objects.get(order_id=order_id, product_id=product_id)
                saved_item.created_at = str(datetime.datetime.today()).replace(" ", "T")
                saved_item.updated_at = str(datetime.datetime.today()).replace(" ", "T")
                saved_item.save()
                saved_prods = OrderItem.objects.filter(order_id=order_id)
                main_order = OrderDetail.objects.get(id=order_id)
                main_update_time = main_order.updated_at
                mod_main_time = main_update_time.split(':')
                usable_main_time = mod_main_time[0] + ':' + mod_main_time[1]
                pre_main_sec = mod_main_time[2].split('.')
                mod_main_sec = pre_main_sec[0]
                for prod in saved_prods:
                    update_time = prod.updated_at
                    mod_time = update_time.split(':')
                    usable_time = mod_time[0] + ':' + mod_time[1]
                    pre_sec = mod_time[2].split('.')
                    mod_sec = pre_sec[0]
                    print(usable_time)
                    print(usable_main_time)
                    print((int(mod_sec) - int(mod_main_sec)))
                    if (usable_time == usable_main_time) and (abs((int(mod_sec) - int(mod_main_sec))) < 10):
                        pass
                    else:
                        prod.delete()
                        print(usable_time)
                        print(usable_main_time)
                        print((int(mod_sec) - int(mod_main_sec)))
                return Response({"status": "success", "data": "Order Placed"})
        else:
            return Response({"status": "invalid", "data": "Enter valid data please."})


class OrderItemSavePutViews(APIView):
    def put(self, request, order_id=None, product_id=None):
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            try:
                item = OrderItem.objects.get(order_id=order_id, product_id=product_id, is_completed=False)
                print(item)
                if item is not None:
                    return Response({"status": "error", "data": "Product already exists"})
            except OrderItem.DoesNotExist:
                serializer.save()
                saved_item = OrderItem.objects.get(order_id=order_id, product_id=product_id)
                saved_item.created_at = str(datetime.datetime.today()).replace(" ", "T")
                saved_item.updated_at = str(datetime.datetime.today()).replace(" ", "T")
                saved_item.save()
                saved_prods = OrderItem.objects.filter(order_id=order_id)
                main_order = OrderDetail.objects.get(id=order_id)
                main_update_time = main_order.updated_at
                mod_main_time = main_update_time.split(':')
                usable_main_time = mod_main_time[0] + ':' + mod_main_time[1]
                pre_main_sec = mod_main_time[2].split('.')
                mod_main_sec = pre_main_sec[0]
                for prod in saved_prods:
                    update_time = prod.updated_at
                    mod_time = update_time.split(':')
                    usable_time = mod_time[0] + ':' + mod_time[1]
                    pre_sec = mod_time[2].split('.')
                    mod_sec = pre_sec[0]
                    print(usable_time)
                    print(usable_main_time)
                    print((int(mod_sec) - int(mod_main_sec)))
                    if (usable_time == usable_main_time) and (abs((int(mod_sec) - int(mod_main_sec))) < 10):
                        pass
                    else:
                        prod.delete()
                        print(usable_time)
                        print(usable_main_time)
                        print((int(mod_sec) - int(mod_main_sec)))
                return Response({"status": "success", "data": "Order Placed"})
        else:
            return Response({"status": "invalid", "data": "Enter valid data please."})


class OrderItemUpdateViews(APIView):
    def patch(self, request, order_id=None, product_id=None):
        try:
            item = OrderItem.objects.get(order_id=order_id, product_id=product_id)
            serializer = OrderItemSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                saved_item = OrderItem.objects.get(order_id=order_id, product_id=product_id)
                saved_item.updated_at = str(datetime.datetime.today()).replace(" ", "T")
                saved_item.save()
                saved_prods = OrderItem.objects.filter(order_id=order_id)
                main_order = OrderDetail.objects.get(id=order_id)
                main_update_time = main_order.updated_at
                mod_main_time = main_update_time.split(':')
                usable_main_time = mod_main_time[0] + ':' + mod_main_time[1]
                pre_main_sec = mod_main_time[2].split('.')
                mod_main_sec = pre_main_sec[0]
                for prod in saved_prods:
                    update_time = prod.updated_at
                    mod_time = update_time.split(':')
                    usable_time = mod_time[0] + ':' + mod_time[1]
                    pre_sec = mod_time[2].split('.')
                    mod_sec = pre_sec[0]
                    print(usable_time)
                    print(usable_main_time)
                    print((int(mod_sec) - int(mod_main_sec)))
                    if (usable_time == usable_main_time) and (abs((int(mod_sec) - int(mod_main_sec))) < 10):
                        pass
                    else:
                        prod.delete()
                        print(usable_time)
                        print(usable_main_time)
                        print((int(mod_sec) - int(mod_main_sec)))
                return Response({"status": "success", "data": "Order Updated"})
            else:
                return Response({"status": "invalid", "data": "Enter valid data please."})
        except OrderItem.DoesNotExist:
            serializer = OrderItemSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                saved_item = OrderItem.objects.get(order_id=order_id, product_id=product_id)
                saved_item.created_at = str(datetime.datetime.today()).replace(" ", "T")
                saved_item.updated_at = str(datetime.datetime.today()).replace(" ", "T")
                saved_item.save()
                saved_prods = OrderItem.objects.filter(order_id=order_id)
                main_order = OrderDetail.objects.get(id=order_id)
                main_update_time = main_order.updated_at
                mod_main_time = main_update_time.split(':')
                usable_main_time = mod_main_time[0] + ':' + mod_main_time[1]
                pre_main_sec = mod_main_time[2].split('.')
                mod_main_sec = pre_main_sec[0]
                for prod in saved_prods:
                    update_time = prod.updated_at
                    mod_time = update_time.split(':')
                    usable_time = mod_time[0] + ':' + mod_time[1]
                    pre_sec = mod_time[2].split('.')
                    mod_sec = pre_sec[0]
                    print(usable_time)
                    print(usable_main_time)
                    print((int(mod_sec) - int(mod_main_sec)))
                    if (usable_time == usable_main_time) and (abs((int(mod_sec) - int(mod_main_sec))) < 10):
                        pass
                    else:
                        prod.delete()
                        print(usable_time)
                        print(usable_main_time)
                        print((int(mod_sec) - int(mod_main_sec)))
                return Response({"status": "non-exist", "data": "New product Added"})


class OrderItemUpdatePutViews(APIView):
    def put(self, request, order_id=None, product_id=None):
        try:
            item = OrderItem.objects.get(order_id=order_id, product_id=product_id)
            serializer = OrderItemSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                saved_item = OrderItem.objects.get(order_id=order_id, product_id=product_id)
                saved_item.updated_at = str(datetime.datetime.today()).replace(" ", "T")
                saved_item.save()
                saved_prods = OrderItem.objects.filter(order_id=order_id)
                main_order = OrderDetail.objects.get(id=order_id)
                main_update_time = main_order.updated_at
                mod_main_time = main_update_time.split(':')
                usable_main_time = mod_main_time[0] + ':' + mod_main_time[1]
                pre_main_sec = mod_main_time[2].split('.')
                mod_main_sec = pre_main_sec[0]
                for prod in saved_prods:
                    update_time = prod.updated_at
                    mod_time = update_time.split(':')
                    usable_time = mod_time[0] + ':' + mod_time[1]
                    pre_sec = mod_time[2].split('.')
                    mod_sec = pre_sec[0]
                    print(usable_time)
                    print(usable_main_time)
                    print((int(mod_sec) - int(mod_main_sec)))
                    if (usable_time == usable_main_time) and (abs((int(mod_sec) - int(mod_main_sec))) < 10):
                        pass
                    else:
                        prod.delete()
                        print(usable_time)
                        print(usable_main_time)
                        print((int(mod_sec) - int(mod_main_sec)))
                return Response({"status": "success", "data": "Order Updated"})
            else:
                return Response({"status": "invalid", "data": "Enter valid data please."})
        except OrderItem.DoesNotExist:
            serializer = OrderItemSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                saved_item = OrderItem.objects.get(order_id=order_id, product_id=product_id)
                saved_item.created_at = str(datetime.datetime.today()).replace(" ", "T")
                saved_item.updated_at = str(datetime.datetime.today()).replace(" ", "T")
                saved_item.save()
                saved_prods = OrderItem.objects.filter(order_id=order_id)
                main_order = OrderDetail.objects.get(id=order_id)
                main_update_time = main_order.updated_at
                mod_main_time = main_update_time.split(':')
                usable_main_time = mod_main_time[0] + ':' + mod_main_time[1]
                pre_main_sec = mod_main_time[2].split('.')
                mod_main_sec = pre_main_sec[0]
                for prod in saved_prods:
                    update_time = prod.updated_at
                    mod_time = update_time.split(':')
                    usable_time = mod_time[0] + ':' + mod_time[1]
                    pre_sec = mod_time[2].split('.')
                    mod_sec = pre_sec[0]
                    print(usable_time)
                    print(usable_main_time)
                    print((int(mod_sec) - int(mod_main_sec)))
                    if (usable_time == usable_main_time) and (abs((int(mod_sec) - int(mod_main_sec))) < 10):
                        pass
                    else:
                        prod.delete()
                        print(usable_time)
                        print(usable_main_time)
                        print((int(mod_sec) - int(mod_main_sec)))
                return Response({"status": "non-exist", "data": "New product Added"})


class GetOrderViews(APIView):
    def get(self, request, customer_name=None):
        try:
            dist_order = OrderDetail.objects.get(customer_name=customer_name)
            order_create_date = dist_order.created_at
            if not is_cart_expired(order_create_date):
                order_id = dist_order.id
                items = OrderItem.objects.filter(order_id=order_id)
                serializer = OrderItemSerializer(items, many=True)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                order_id = dist_order.id
                items = OrderItem.objects.filter(order_id=order_id)
                for prod in items:
                    prod.delete()
                dist_order.delete()
                return Response({"status": "error", "data": "Order has expired"})
        except (OrderDetail.DoesNotExist, OrderItem.DoesNotExist):
            return Response({"status": "error", "data": "Order does not exist"},
                            status=status.HTTP_400_BAD_REQUEST)


class GetOrderByIdViews(APIView):
    def get(self, request, order_id=None):
        try:
            dist_order = OrderDetail.objects.get(id=order_id)
            order_create_date = dist_order.created_at
            if not is_cart_expired(order_create_date):
                shipping_fee = dist_order.shipping_fee
                total_price = dist_order.total_price
                customer_id = dist_order.customer_id
                is_customer = dist_order.is_customer
                payment_id = dist_order.payment_id
                pay_data = {
                    "shipping_fee": shipping_fee,
                    "total_price": total_price,
                    "customer_id": customer_id,
                    "is_customer": is_customer,
                    "payment_id": payment_id
                }
                return Response({"status": "success", "data": pay_data}, status=status.HTTP_200_OK)
            else:
                order_id = dist_order.id
                items = OrderItem.objects.filter(order_id=order_id)
                for prod in items:
                    prod.delete()
                dist_order.delete()
                return Response({"status": "error", "data": "Order has expired"})
        except (OrderDetail.DoesNotExist, OrderItem.DoesNotExist):
            return Response({"status": "error", "data": "Order does not exist"},
                            status=status.HTTP_400_BAD_REQUEST)


class DelOrderViews(APIView):
    def delete(self, request, order_id=None):
        item = get_object_or_404(OrderDetail, id=order_id)
        ord_id = item.id
        prods = OrderItem.objects.filter(order_id=ord_id)
        for prod in prods:
            prod.delete()
        item.delete()
        return Response({"status": "success", "data": "Order Items Deleted"})


class PaymentDetailViews(APIView):
    def post(self, request, order_id=None):
        serializer = PaymentDetailSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            try:
                payment = PaymentDetail.objects.get(order_id=order_id)
                if payment is not None:
                    return Response({"status": "error", "data": "Payment detail already exists"})
            except PaymentDetail.DoesNotExist:
                serializer.save()
                saved_payment = PaymentDetail.objects.get(order_id=order_id)
                saved_payment.created_at = str(datetime.datetime.today()).replace(" ", "T")
                saved_payment.updated_at = str(datetime.datetime.today()).replace(" ", "T")
                payment_id = saved_payment.id
                saved_payment.save()
                mod_order = OrderDetail.objects.get(id=order_id)
                mod_order.payment_id = payment_id
                mod_order.save()
                return Response({"status": "success", "data": "Payment detail created"})
        else:
            return Response({"status": "invalid", "data": "Enter valid data please."})


class PaymentDetailUpdateViews(APIView):
    def patch(self, request, order_id=None):
        try:
            payment = PaymentDetail.objects.get(order_id=order_id)
            serializer = PaymentDetailSerializer(payment, data=request.data, partial=True)
            if serializer.is_valid():
                payment_create_date = payment.created_at
                if not is_cart_expired(payment_create_date):
                    serializer.save()
                    payment.updated_at = str(datetime.datetime.today()).replace(" ", "T")
                    payment.save()
                    return Response({"status": "success", "data": "Payment detail updated"})
                else:
                    payment.delete()
                    return Response({"status": "error", "data": "Payment detail has expired"})
            else:
                return Response({"status": "invalid", "data": "Enter valid data please."})
        except PaymentDetail.DoesNotExist:
            return Response({"status": "non-exist", "data": "Payment detail does not exist"})


class PaymentDetailUpdatePutViews(APIView):
    def put(self, request, order_id=None):
        try:
            payment = PaymentDetail.objects.get(order_id=order_id)
            serializer = PaymentDetailSerializer(payment, data=request.data, partial=True)
            if serializer.is_valid():
                payment_create_date = payment.created_at
                if not is_cart_expired(payment_create_date):
                    serializer.save()
                    payment.updated_at = str(datetime.datetime.today()).replace(" ", "T")
                    payment.save()
                    return Response({"status": "success", "data": "Payment detail updated"})
                else:
                    payment.delete()
                    return Response({"status": "error", "data": "Payment detail has expired"})
            else:
                return Response({"status": "invalid", "data": "Enter valid data please."})
        except PaymentDetail.DoesNotExist:
            return Response({"status": "non-exist", "data": "Payment detail does not exist"})


class GetReadyOrdersViews(APIView):
    def get(self, request):
        ready_orders = OrderDetail.objects.filter(is_completed=True, is_dispatched=False)
        serializer = OrderDetailSerializer(ready_orders, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class GetDispatchableOrderItemsViews(APIView):
    def get(self, request, order_id=None):
        dispatchable_items = OrderItem.objects.filter(order_id=order_id)
        serializer = OrderItemSerializer(dispatchable_items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class UpdateOrderDispatchedViews(APIView):
    def patch(self, request, order_id=None):
        try:
            dispatched_order = OrderDetail.objects.get(id=order_id)
            serializer = OrderDetailSerializer(dispatched_order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "data": "Order has been dispatched"})
            else:
                print(serializer.errors)
        except OrderDetail.DoesNotExist:
            return Response({"status": "error", "data": "Order does not exist"})


class UpdateOrderDispatchedMobileViews(APIView):
    def put(self, request, order_id=None):
        try:
            dispatched_order = OrderDetail.objects.get(id=order_id)
            serializer = OrderDetailSerializer(dispatched_order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                dispatched_order.updated_at = str(datetime.datetime.today()).replace(" ", "T")
                dispatched_order.save()
                return Response({"status": "success", "data": "Order has been dispatched"})
            else:
                print(serializer.errors)
        except OrderDetail.DoesNotExist:
            return Response({"status": "error", "data": "Order does not exist"})
