from django.contrib import admin
from .models import (Product,
                      product_arrival,
                      product_shipment,
                      Import_products,
                      import_product_shipment)

admin.site.register(Product)
admin.site.register(product_arrival)
admin.site.register(product_shipment)
admin.site.register(Import_products)
admin.site.register(import_product_shipment)