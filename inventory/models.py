import datetime
from datetime import datetime as dt
from django.db import models
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, default='Резцы')
    quantity = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-name']

    def get_queryset(self, request):
        if not request.user.IsNotManager():
            qs = super(Product, self).get_queryset(request)
            print(qs)
            filtered_qs = qs.filter(category="Резцы")
            print(filtered_qs)
            return filtered_qs
        else:
            qs = super(Product, self).get_queryset(request)
            print("qs: ", qs)
            return qs


class Import_products(models.Model):
    name = models.CharField(max_length=400)
    description = models.TextField(blank=True)
    gtd_id = models.CharField(max_length=100)
    date = models.DateField(blank=False)
    #third_id = models.IntegerField(blank=False)
    category = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    income_quantity = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-name']

class import_product_shipment(models.Model):
    reciever = models.CharField(max_length=100)
    date = models.DateField(blank=False)
    quantity = models.IntegerField(default=0)
    product_id = models.CharField(max_length=100)
    billing_number = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.product_id


class product_arrival(models.Model):
    supplier = models.CharField(max_length=100)
    date = models.DateField(blank=True, default=dt.now())
    quantity = models.IntegerField(default=0)
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class product_shipment(models.Model):
    reciever = models.CharField(max_length=100)
    date = models.DateField(blank=True)
    quantity = models.IntegerField(default=0)
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name
