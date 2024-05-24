import datetime
from datetime import datetime as dt
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, default='Резцы')
    quantity = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name


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
