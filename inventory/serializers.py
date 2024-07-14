from rest_framework import serializers
from inventory import models


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['id', 'name', 'quantity', 'income_price', 'minimal_price', 'category']


class ImportproductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Import_products
        fields = ['id', 'name', 'description', 'gtd_id', 'date', 'category', 'quantity', "income_quantity"]#'third_id',


class ImportproductsShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.import_product_shipment
        fields = ['id', 'reciever', 'date', 'quantity', 'product_id', 'billing_number']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.product_arrival
        fields = ['id', 'supplier', 'date', 'quantity', 'name']


class ProductShipment(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.product_shipment
        fields = ['id', 'reciever', 'date', 'quantity', 'name']
