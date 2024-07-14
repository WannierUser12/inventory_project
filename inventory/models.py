import datetime
from datetime import datetime as dt
from django.db import models
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=100)
    income_price = models.CharField(default=0)
    minimal_price = models.CharField(default=0)
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
    category = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    income_quantity = models.IntegerField(default=0)
    income_price = models.CharField(max_length=100, default=0)
    minimal_price = models.CharField(max_length=100, default=0)

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
    date = models.DateField(blank=True)
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


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
