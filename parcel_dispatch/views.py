import asyncio
import datetime
import json

import httpx
import rest_framework
from asgiref.sync import sync_to_async
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DispatchedProduct, DispatchDetail
from .serializers import DispatchItemsSerializer, DispatchDetailSerializer, DispatchedProductSerializer

# Create your views here.
# from httpx import Response
from rest_framework.views import APIView


def dispatch(request):
    return render(request, "parcel_dispatch\\dispatch.html")


def get_products(request):
    context = {
        "data": []
    }
    try:
        response = httpx.get('http://localhost:7000/parcel_product/get_sing_prod/2/')
        if response.status_code == httpx.codes.OK:
            context['data'] = response.json()
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}.")
    return render(request, "parcel_dispatch\\dispatch.html", context)


#
# async def fetching_order():
#     context = {
#         "ready_orders": []
#     }
#     try:
#         async with httpx.AsyncClient() as client:
#             response = client.get('http://localhost:7000/parcel_order/get_ready_orders/')
#             # if response.status_code == httpx.codes.OK:
#             context['ready_orders'] = response
#             # context['ready_orders'] = response.json()
#             # print(response.json())
#             # print(context)
#             return context
#     except httpx.RequestError as exc:
#         print(f"An error occurred while requesting {exc.request.url!r}.")
#
#
# async def get_ready_orders(request):
#     context = await asyncio.run(fetching_order())
#
#     return render(request, "parcel_dispatch\\dispatch.html", context)


@sync_to_async()
def save_dispatched_products(order_id, product_id, each_product):
    try:
        find_prod_array = DispatchedProduct.objects.get(order_id=order_id,
                                                        product_id=product_id)
        if find_prod_array is not None:
            pass
    except DispatchedProduct.DoesNotExist:
        p = each_product
        new_prod_array = DispatchedProduct(order_id=p['order_id'],
                                           product_id=p['product_id'],
                                           is_supply_ready=False,
                                           is_supply_received=False,
                                           is_delivered=p['is_delivered'],
                                           is_received=p['is_received'],
                                           prod_model=p['prod_model'],
                                           product_name=p['product_name'],
                                           quantity=p['quantity'],
                                           prod_price=p['prod_price'],
                                           prod_photo=p['prod_photo'],
                                           total_amount=p['total_amount'],
                                           vendor_email=p['vendor_email'],
                                           vendor_phone=p['vendor_phone'],
                                           vendor_name=p['vendor_name'],
                                           vendor_address=p['vendor_address'],
                                           created_at=f"{datetime.datetime.today()}",
                                           updated_at=f"{datetime.datetime.today()}")
        new_prod_array.save()


@sync_to_async()
def save_dispatch_detail(order_id, single_dispatch):
    try:
        find_order = DispatchDetail.objects.get(order_id=order_id)
        if find_order is not None:
            pass
    except DispatchDetail.DoesNotExist:
        d = single_dispatch
        new_dispatch = DispatchDetail(order_id=d['order_id'],
                                      customer_id=d['customer_id'],
                                      customer_name=d['customer_name'],
                                      address=d['address'],
                                      email=d['email'],
                                      phone_no=d['phone_no'],
                                      is_customer=d['is_customer'],
                                      is_delivered=d['is_delivered'],
                                      is_received=d['is_received'],
                                      shipping_method=d['shipping_method'],
                                      total_items=d['total_items'],
                                      total_price=d['total_price'],
                                      zip_code=d['zip_code'],
                                      handled_dispatch=False,
                                      courier_id="000",
                                      courier_name="000",
                                      courier_phone="000",
                                      courier_email="000",
                                      created_at=f"{datetime.datetime.today()}",
                                      updated_at=f"{datetime.datetime.today()}"
                                      )
        new_dispatch.save()


async def get_ready_orders(request):
    dispatch_array = []
    context = {
        "dispatch_array": dispatch_array
    }
    try:
        async with httpx.AsyncClient() as client:
            fetch_order = await client.get('http://localhost:7000/parcel_order/get_ready_orders/')
            if fetch_order.status_code == httpx.codes.OK:
                raw_order = fetch_order.json()
                orders = raw_order['data']
                for order in orders:
                    if order['is_dispatched'] is False:
                        purchased_products = []
                        single_dispatch = {}
                        single_dispatch['order_id'] = order['id']
                        single_dispatch['customer_id'] = order['customer_id']
                        single_dispatch['customer_name'] = order['customer_name']
                        single_dispatch['total_items'] = order['total_items']
                        single_dispatch['total_price'] = order['total_price']
                        single_dispatch['is_customer'] = order['is_customer']
                        single_dispatch['zip_code'] = order['zip_code']
                        single_dispatch['shipping_method'] = order['shipping_method']
                        single_dispatch['is_delivered'] = False
                        single_dispatch['is_received'] = False
                        single_dispatch['handled_dispatch'] = False
                        single_dispatch['courier_id'] = "000"
                        single_dispatch['courier_email'] = "000"
                        single_dispatch['courier_phone'] = "000"
                        single_dispatch['courier_name'] = "000"

                        if order['is_customer']:
                            try:
                                fetch_customer = await client.get(
                                    f"http://localhost:7000/parcel_customer/get_customer/{order['customer_id']}/")
                                if fetch_customer.status_code == httpx.codes.OK:
                                    raw_customer = fetch_customer.json()
                                    customer = raw_customer['data']
                                    customer_address = customer['street'] + ", " + customer['state'] + ", " + customer[
                                        'country']
                                    single_dispatch['address'] = customer_address
                                    single_dispatch['phone_no'] = customer['phone_no']
                                    single_dispatch['email'] = customer['email']
                            except httpx.RequestError as exa:
                                print(f"An error occurred while requesting {exa.request.url!r}.")
                        else:
                            try:
                                fetch_customer = await client.get(
                                    f"http://localhost:7000/parcel_customer/get_anon_customer/{order['customer_id']}/")
                                if fetch_customer.status_code == httpx.codes.OK:
                                    raw_customer = fetch_customer.json()
                                    customer = raw_customer['data']
                                    customer_address = customer['street'] + ", " + customer['state'] + ", " + customer[
                                        'country']
                                    single_dispatch['address'] = customer_address
                                    single_dispatch['phone_no'] = customer['phone_no']
                                    single_dispatch['email'] = customer['email']
                            except httpx.RequestError as exb:
                                print(f"An error occurred while requesting {exb.request.url!r}.")
                        try:
                            fetch_order_items = await client.get(
                                f"http://localhost:7000/parcel_order/get_dispatchable_items/{order['id']}/")
                            if fetch_order_items.status_code == httpx.codes.OK:
                                raw_order_items = fetch_order_items.json()
                                order_items = raw_order_items['data']
                                for order_item in order_items:
                                    each_product = {}
                                    each_product['order_id'] = order_item['order_id']
                                    each_product['product_id'] = order_item['product_id']
                                    each_product['product_name'] = order_item['product_name']
                                    each_product['quantity'] = order_item['quantity']
                                    each_product['is_delivered'] = False
                                    each_product['is_received'] = False

                                    try:
                                        fetch_product = await client.get(
                                            f"http://localhost:7000/parcel_product/get_sing_prod/{order_item['product_id']}/")
                                        if fetch_product.status_code == httpx.codes.OK:
                                            raw_product = fetch_product.json()
                                            product = raw_product['data']
                                            each_product['prod_price'] = product['prod_price']
                                            each_product['prod_model'] = product['prod_model']
                                            each_product['vendor_phone'] = product['vendor_phone']
                                            each_product['vendor_name'] = product['vendor_name']
                                            each_product['vendor_email'] = product['vendor_email']
                                            each_product['prod_photo'] = product['prod_photo']
                                            each_product['total_amount'] = product['prod_price'] * order_item[
                                                'quantity']

                                            try:
                                                fetch_vendor = await client.get(
                                                    f"http://localhost:7000/parcel_backends/get_ven_email/{product['vendor_email']}/")
                                                if fetch_vendor.status_code == httpx.codes.OK:
                                                    raw_vendor = fetch_vendor.json()
                                                    vendor = raw_vendor['data']
                                                    vendor_address = vendor['bus_street'] + ", " + vendor[
                                                        'bus_state'] + ", " + vendor['bus_country']
                                                    each_product['vendor_address'] = vendor_address
                                            except httpx.RequestError as exv:
                                                print(f"An error occurred while requesting {exv.request.url!r}.")

                                            purchased_products.append(each_product)
                                            await save_dispatched_products(order['id'], order_item['product_id'],
                                                                           each_product)

                                            single_dispatch['products'] = purchased_products
                                    except httpx.RequestError as exf:
                                        print(f"An error occurred while requesting {exf.request.url!r}.")
                            dispatch_array.append(single_dispatch)
                            await save_dispatch_detail(order['id'], single_dispatch)

                        except httpx.RequestError as exd:
                            print(f"An error occurred while requesting {exd.request.url!r}.")
    except httpx.RequestError as ex:
        print(f"An error occurred while requesting {ex.request.url!r}.")
    return JsonResponse(context, safe=True)


class SaveDispatchDetailViews(APIView):
    def post(self, request, order_id=None):
        serializer = DispatchDetailSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            try:
                dispatch_detail = DispatchDetail.objects.get(order_id=order_id)
                if dispatch_detail is not None:
                    return Response({"status": "error", "data": "Dispatch detail already exists"})
            except DispatchDetail.DoesNotExist:
                serializer.save()
                return Response({"status": "success", "data": "Dispatch detail saved"})
        else:
            print(serializer.errors)


class UpdateDispatchDetailViews(APIView):
    def patch(self, request, order_id=None):
        try:
            dispatch_detail = DispatchDetail.objects.get(order_id=order_id)
            serializer = DispatchDetailSerializer(dispatch_detail, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "data": "Dispatch detail updated"})
            else:
                print(serializer.errors)
        except DispatchDetail.DoesNotExist:
            return Response({"status": "non-exist", "data": "Payment detail does not exist"})


class UpdateDispatchDetailMobileViews(APIView):
    def put(self, request, order_id=None):
        try:
            dispatch_detail = DispatchDetail.objects.get(order_id=order_id)
            serializer = DispatchDetailSerializer(dispatch_detail, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                dispatch_detail.updated_at = str(datetime.datetime.today()).replace(" ", "T")
                dispatch_detail.save()
                return Response({"status": "success", "data": "Dispatch detail updated"})
            else:
                print(serializer.errors)
        except DispatchDetail.DoesNotExist:
            return Response({"status": "non-exist", "data": "Payment detail does not exist"})


class SaveDispatchedProductViews(APIView):
    def post(self, request, order_id=None, product_id=None):
        serializer = DispatchedProductSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            try:
                dispatched_product = DispatchedProduct.objects.get(order_id=order_id, product_id=product_id)
                if dispatched_product is not None:
                    return Response({"status": "error", "data": "Product detail already exists"})
            except DispatchedProduct.DoesNotExist:
                serializer.save()
                return Response({"status": "success", "data": "Product saved"})
        else:
            print(serializer.errors)


class UpdateDispatchedProductViews(APIView):
    def patch(self, request, order_id=None, product_id=None):
        try:
            dispatched_product = DispatchedProduct.objects.get(order_id=order_id, product_id=product_id)
            serializer = DispatchDetailSerializer(dispatched_product, data=request.data, partial=True)
            if serializer.is_valid():
                print(request.data)
                serializer.save()
                return Response({"status": "success", "data": "Delivery status updated"})
            else:
                print(serializer.errors)
        except DispatchedProduct.DoesNotExist:
            return Response({"status": "non-exist", "data": "Product is not part of the order"})


class UpdateDispatchedProductMobileViews(APIView):
    def put(self, request, order_id=None, product_id=None):
        try:
            dispatched_product = DispatchedProduct.objects.get(order_id=order_id, product_id=product_id)
            serializer = DispatchDetailSerializer(dispatched_product, data=request.data, partial=True)
            if serializer.is_valid():
                print(request.data)
                serializer.save()
                dispatched_product.updated_at = str(datetime.datetime.today()).replace(" ", "T")
                dispatched_product.save()
                return Response({"status": "success", "data": "Delivery status updated"})
            else:
                print(serializer.errors)
        except DispatchedProduct.DoesNotExist:
            return Response({"status": "non-exist", "data": "Product is not part of the order"})


def get_dispatches_views(request):
    dispatches = DispatchDetail.objects.all()
    mod_dispatch = []
    data = {
        "deals": mod_dispatch
    }
    for item in dispatches:
        single_dispatch = {}
        single_dispatch['order_id'] = item.order_id
        single_dispatch['customer_id'] = item.customer_id
        single_dispatch['customer_name'] = item.customer_name
        single_dispatch['total_items'] = item.total_items
        single_dispatch['total_price'] = item.total_price
        single_dispatch['is_customer'] = item.is_customer
        single_dispatch['zip_code'] = item.zip_code
        single_dispatch['shipping_method'] = item.shipping_method
        single_dispatch['is_delivered'] = item.is_delivered
        single_dispatch['is_received'] = item.is_received
        single_dispatch['handled_dispatch'] = item.handled_dispatch
        single_dispatch['courier_id'] = item.courier_id
        single_dispatch['courier_email'] = item.courier_email
        single_dispatch['courier_phone'] = item.courier_phone
        single_dispatch['courier_name'] = item.courier_name
        single_dispatch['address'] = item.address
        single_dispatch['phone_no'] = item.phone_no
        single_dispatch['email'] = item.email
        single_dispatch['created_at'] = item.created_at
        single_dispatch['updated_at'] = item.updated_at

        prod_collec = []
        dispatched_products = DispatchedProduct.objects.filter(order_id=item.order_id)
        for collec in dispatched_products:
            if collec.order_id == item.order_id:
                each_product = {}
                each_product['order_id'] = collec.order_id
                each_product['product_id'] = collec.product_id
                each_product['product_name'] = collec.product_name
                each_product['quantity'] = collec.quantity
                each_product['is_supply_ready'] = collec.is_supply_ready
                each_product['is_supply_received'] = collec.is_supply_received
                each_product['is_delivered'] = collec.is_delivered
                each_product['is_received'] = collec.is_received
                each_product['prod_price'] = collec.prod_price
                each_product['prod_model'] = collec.prod_model
                each_product['vendor_phone'] = collec.vendor_phone
                each_product['vendor_name'] = collec.vendor_name
                each_product['vendor_email'] = collec.vendor_email
                each_product['prod_photo'] = collec.prod_photo
                each_product['total_amount'] = collec.total_amount
                each_product['vendor_address'] = collec.vendor_address
                each_product['created_at'] = collec.created_at
                each_product['updated_at'] = collec.updated_at
                prod_collec.append(each_product)
        single_dispatch['products'] = prod_collec
        mod_dispatch.append(single_dispatch)
    return JsonResponse(data, safe=True)


@csrf_exempt
def update_supply_ready(request, order_id=None, product_id=None):
    if request.method == 'POST':
        try:
            supply = DispatchedProduct.objects.get(order_id=order_id, product_id=product_id)
            if supply is not None:
                form_input = request.POST
                print(form_input['is_supply_ready'])
                supply.is_supply_ready = False
                if form_input['is_supply_ready'] == "true":
                    supply.is_supply_ready = True
                elif form_input['is_supply_ready'] == "false":
                    supply.is_supply_ready = False
                supply.updated_at = form_input['updated_at']
                supply.save()
                return JsonResponse({"status": "success", "data": "Supply detail updated"}, safe=True)
        except DispatchedProduct.DoesNotExist:
            return JsonResponse({"status": "error", "data": "Product does not exist"}, safe=True)


@csrf_exempt
def update_supply_received(request, order_id=None, product_id=None):
    if request.method == 'POST':
        try:
            supply = DispatchedProduct.objects.get(order_id=order_id, product_id=product_id)
            if supply is not None:
                form_input = request.POST
                print(form_input['is_supply_received'])
                supply.is_supply_received = False
                if form_input['is_supply_received'] == "true":
                    supply.is_supply_received = True
                elif form_input['is_supply_received'] == "false":
                    supply.is_supply_received = False
                supply.updated_at = form_input['updated_at']
                supply.save()
                return JsonResponse({"status": "success", "data": "Supply detail updated"}, safe=True)
        except DispatchedProduct.DoesNotExist:
            return JsonResponse({"status": "error", "data": "Product does not exist"}, safe=True)
