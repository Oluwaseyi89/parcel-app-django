import datetime
from datetime import date, timedelta

from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from django.core.files.storage import FileSystemStorage
from .models import TempProduct, Product
from .serializers import TempProductSerializer, ProductSerializer, ProductUpdateSerializer
from django.http import HttpResponse


# Create your views here.
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


def product(request):
    return render(request, "parcel_product\\product.html")


class TempProductViews(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):
        serializer = TempProductSerializer(data=request.data)
        if serializer.is_valid():
            try:
                p_prod = TempProduct.objects.get(img_base=request.data['img_base'],
                                                 vendor_email=request.data['vendor_email'])
                if p_prod is not None:
                    return Response({"status": "error", "data": "Product already uploaded but yet to be approved."})
            except TempProduct.DoesNotExist:
                try:
                    prod = Product.objects.get(img_base=request.data['img_base'],
                                               vendor_email=request.data['vendor_email'])
                    if prod is not None:
                        return Response({"status": "error", "data": "Product already uploaded and approved."})
                except Product.DoesNotExist:
                    upload = request.FILES['prod_photo']
                    fss = FileSystemStorage()
                    file = fss.save(upload.name, upload)
                    file_url = fss.url(file)
                    print(file_url)
                    print(upload.name)
                    serializer.save()
                    p_prod = TempProduct.objects.get(img_base=request.data['img_base'],
                                                     vendor_email=request.data['vendor_email'])
                    p_prod.upload_date = str(datetime.datetime.today()).replace(" ", "T")
                    p_prod.save()
                    return Response({"status": "success", "data": "Product uploaded successfully."},
                                    status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": "Unable to save your product. "
                                                        "Please refresh and enter proper data."},
                            status=status.HTTP_400_BAD_REQUEST)


class ProductViews(APIView):
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            try:
                prod = Product.objects.get(vendor_email=request.data['vendor_email'],
                                           img_base=request.data['img_base'])
                if prod is not None:
                    return Response({"status": "error", "data": "Product Already Approved"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except Product.DoesNotExist:
                serializer.save()
                return Response({"status": "success", "data": "Product Approved"}, status=status.HTTP_200_OK)


class GetTempProductViews(APIView):
    def get(self, request, id=None):
        p_products = TempProduct.objects.all()
        serializer = TempProductSerializer(p_products, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class GetProductViews(APIView):
    def get(self, request):
        products = Product.objects.filter(prod_qty__gt=0)
        updated_prods = []
        for item in products:
            if date.today() <= (make_date(item.updated_at) + timedelta(days=3)):
                updated_prods.append(item)
        serializer = ProductSerializer(updated_prods, many=True)
        # serializer = ProductSerializer(products, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class GetSingleProductViews(APIView):
    def get(self, request, id=None):
        products = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(products)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class DelTempProductViews(APIView):
    def delete(self, request, id=None):
        item = get_object_or_404(TempProduct, id=id)
        item.delete()
        return Response({"status": "success", "data": "Temporary Product Deleted"})


class GetDistinctVendorProductViews(APIView):
    def get(self, request, vendor_email=None):
        try:
            dist_vend_prod = Product.objects.filter(vendor_email=vendor_email)
            serializer = ProductSerializer(dist_vend_prod, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"status": "error", "data": "You are yet to upload any product"},
                            status=status.HTTP_400_BAD_REQUEST)


class ProductUpdateViews(APIView):
    def post(self, request, id=None):
        serializer = ProductUpdateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                prod = Product.objects.get(id=id)
                if prod is not None:
                    prod.prod_price = request.data['prod_price']
                    prod.prod_qty = request.data['prod_qty']
                    prod.prod_disc = request.data['prod_disc']
                    prod.updated_at = str(datetime.datetime.today()).replace(" ", "T")
                    prod.save()
                    return Response({"status": "success", "data": "Product Updated"},
                                    status=status.HTTP_200_OK)

            except Product.DoesNotExist:
                return Response({"status": "error", "data": "Product does not exist"},
                                status=status.HTTP_400_BAD_REQUEST)


class DelProductViews(APIView):
    def delete(self, request, id=None):
        item = get_object_or_404(Product, id=id)
        item.delete()
        return Response({"status": "success", "data": "Product Deleted"})


class GetDistinctVendTempProductViews(APIView):
    def get(self, request, vendor_email=None):
        try:
            dist_vend_prod = TempProduct.objects.filter(vendor_email=vendor_email)
            serializer = TempProductSerializer(dist_vend_prod, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"status": "error", "data": "You are yet to upload any product"},
                            status=status.HTTP_400_BAD_REQUEST)


my_date = make_date('2022-06-19T15:58:25.197Z')
print(my_date)
cpr_date = date.today()
print(cpr_date)
print(my_date == cpr_date)
