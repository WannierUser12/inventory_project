from rest_framework import serializers
from inventory import models


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['id', 'name', 'quantity', 'description', 'category']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.product_arrival
        fields = ['id', 'supplier', 'date', 'quantity', 'name']


class ProductShipment(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.product_shipment
        fields = ['id', 'reciever', 'date', 'quantity', 'name']
