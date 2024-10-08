from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import pandas as pd
from .utils import XLSXSave
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, generics, mixins
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsNotManager
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.decorators import action
from rest_framework.response import Response
from core.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from .forms import DocumentForm
from inventory.models import (Product,
                              product_arrival,
                              product_shipment,
                              Import_products,
                              import_product_shipment)
from inventory.serializers import (ProductSerializer,
                                   ProductShipment,
                                   InventorySerializer,
                                   ImportproductsSerializer,
                                   ImportproductsShipmentSerializer)

from datetime import datetime


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = InventorySerializer
    http_method_names = ['get', 'post', 'put']
    filter_backends = [DjangoFilterBackend]
    def list(self, request, *args, **kwargs):
        if request.user.groups.filter(name='managers').exists():

            filterset_fields = ["Резцы", "Резцедержатели", "Ножи", "Базы", "Болты", "Техпластины", "Прочее"]
            queryset = self.filter_queryset(self.get_queryset()).filter(category__in = filterset_fields)
        else:
            filterset_fields = ["Резцы", "Резцедержатели", "Ножи", "Базы", "Болты", "Техпластины", "Прочее", "Примэкс"]
            queryset = self.filter_queryset(self.get_queryset()).filter(category__in = filterset_fields)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_object(self, request):
        if request.user.IsNotManager():
            queryset = self.get_queryset().filter(category='Резцы')
        else:
            queryset = self.get_queryset().filter(category='Ножи')
        print(queryset)
        return get_object_or_404(queryset, pk=self.kwargs[self.lookup_field])

    def create(self, request, *args, **kwargs):
        if not IsNotManager().has_permission(request, self):
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        print(request.data)
        return super().create(request, *args, **kwargs)

    def create_custom_record(self, request):
        if not IsNotManager().has_permission(request, self):
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # print("POSTED HERE")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImportproductsViewSet(viewsets.ModelViewSet):
    queryset = Import_products.objects.all()
    serializer_class = ImportproductsSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='managers').exists():
            queryset = self.filter_queryset(self.get_queryset()).filter()
        else:
            queryset = self.filter_queryset(self.get_queryset()).filter()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        # print(serializer.data)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not IsNotManager().has_permission(request, self):
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not IsNotManager().has_permission(request, self):
            return Response({"detail": "Permission denied0."}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='shipments_by_description/(?P<product_id>[^/.]+)')
    def get_shipments_by_description(self, request, product_id=None):
        if not product_id:
            return Response({"detail": "product_id parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        shipments = import_product_shipment.objects.filter(product_id=product_id)
        serializer = ImportproductsShipmentSerializer(shipments, many=True)
        return Response(serializer.data)

    def create_custom_record(self, request):
        # if not IsNotManager().has_permission(request, self):
        #     return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            uploaded_file = request.FILES['document']
            data = pd.read_excel(uploaded_file)
            try:
                XLSXSave.save_data_with_user(data, request.user)
                # print('data_exported into db')
                return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'success': False, 'errors': str(e)})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        return JsonResponse({'error': 'Метод не разрешен'}, status=405)



class ImportproductsManagerViewSet(viewsets.ModelViewSet):
    queryset = Import_products.objects.all()
    serializer_class = ImportproductsSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='managers').exists():
            queryset = self.filter_queryset(self.get_queryset()).filter()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ImportproductsShipmentViewSet(viewsets.ModelViewSet):
    queryset = import_product_shipment.objects.all()
    serializer_class = ImportproductsShipmentSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        try:
            product = Import_products.objects.get(id=product_id)
        except Import_products.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        new_quantity = product.quantity - int(request.data.get('quantity'))
        product.quantity = new_quantity
        product.save()

        shipment = import_product_shipment.objects.create(
            product_id=request.data.get('product_id'),
            date=request.data.get('date'),
            reciever=request.data.get('reciever'),
            quantity=request.data.get('quantity'),
            billing_number=request.data.get('billing_number')
        )
        return Response({"detail": "Shipment created successfully."}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='(?P<product_id>[^/.]+)')
    def get_shipments_by_description(self, request, product_id=None):
        if not product_id:
            return Response({"detail": "Description parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        shipments = import_product_shipment.objects.filter(product_id=product_id)  # Здесь предполагается, что модель отгрузок называется Shipment
        serializer = ImportproductsShipmentSerializer(shipments, many=True)
        return Response(serializer.data)


#Продукт
class ProductViewSet(viewsets.ModelViewSet):
    queryset = product_arrival.objects.all()
    serializer_class = ProductSerializer

    def get_object(self):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.kwargs[self.lookup_field])

    @permission_classes([IsAuthenticated, IsNotManager])
    def perform_create(self, request):
        pass


class ArrivalMixinView(viewsets.GenericViewSet,
                       generics.ListCreateAPIView,
                       mixins.RetrieveModelMixin):

    queryset = product_arrival.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if not IsNotManager().has_permission(request, self):
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
        product_name = serializer.validated_data.get("name")
        product_quantity = serializer.validated_data.get("quantity")
        product_category = serializer.validated_data.get("category")

        if product_name and product_quantity:
            try:
                product = Product.objects.filter(name=product_name).first()
                product_quantity = int(product_quantity)
                if product:
                    product.quantity += product_quantity
                    product.save()
                else:
                    new_product_data = {
                        "name": product_name,
                        "quantity": product_quantity,
                        "description": " ",
                        "category": product_category,
                    }
                    inventory_serializer = InventorySerializer(data=new_product_data)
                    if inventory_serializer.is_valid():
                        inventory_serializer.save()
                    else:
                        return Response(inventory_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({"error": "Invalid quantity value"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def filter_by_dates(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if start_date:
            try:
                if start_date and end_date:
                    start_date = datetime.strptime(start_date, '%Y-%m-%d')
                    end_date = datetime.strptime(end_date, '%Y-%m-%d')
                    user = request.user
                    user_groups = user.groups.values_list('name', flat=True)  # TODO
                    queryset = self.queryset.filter(date__range=[start_date, end_date])
                    serializer = self.serializer_class(queryset, many=True)
                    if serializer.data:
                        return Response(serializer.data)
                    else:
                        return Response({"error": "Неверно указаны даты"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            self.get(request)


class ShippingMixinView(viewsets.GenericViewSet,
                        generics.ListCreateAPIView,
                        mixins.RetrieveModelMixin):
    queryset = product_shipment.objects.all()
    serializer_class = ProductShipment

    def get(self, request, *args, **kwargs):
        print(args, kwargs)
        return self.list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if not IsNotManager().has_permission(request, self):
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
        product_name = serializer.validated_data.get("name")
        product_quantity = serializer.validated_data.get("quantity")

        if product_name and product_quantity:
            try:
                product_quantity = int(product_quantity)
                # print('minus ', product_quantity)
                product = Product.objects.filter(name=product_name).first()
                if product:
                    product.quantity -= product_quantity
                    # print(product.quantity)
                    # print(product)
                    product.save()
                    return Response({"ok": "Invalid quantity value"}, status=status.HTTP_200_OK)
            except ValueError:
                return Response({"error": "Invalid quantity value"}, status=status.HTTP_400_BAD_REQUEST)


def arrival(request):
    user_is_manager = request.user.groups.filter(name='managers').exists()
    return render(request, 'inventory/index_arrival.html', {'user_is_manager': user_is_manager})


def proforms(request):
    user_is_manager = request.user.groups.filter(name='managers').exists()
    return render(request, 'inventory/HTMLPage1.html', {'user_is_manager': user_is_manager})


def import_products(request):
    user_is_manager = request.user.groups.filter(name='managers').exists()
    if user_is_manager:
        return render(request, 'inventory/import_products_managers.html', {'user_is_manager': user_is_manager})

    else:
        return render(request, 'inventory/import_products.html', {'user_is_manager': user_is_manager})


def import_products_managers(request):
    user_is_manager = request.user.groups.filter(name='managers').exists()
    return (
        render(request, 'inventory/import_products_managers.html', {'user_is_manager': user_is_manager}))


def index(request):
    user_is_manager = request.user.groups.filter(name='managers').exists()
    return render(request, 'inventory/index.html', {'user_is_manager': user_is_manager})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'inventory/product_detail.html', {'product': product})


