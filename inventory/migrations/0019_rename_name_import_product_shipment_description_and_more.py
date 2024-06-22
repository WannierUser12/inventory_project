# Generated by Django 5.0.6 on 2024-06-19 15:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0018_import_product_shipment_alter_product_arrival_date"),
    ]

    operations = [
        migrations.RenameField(
            model_name="import_product_shipment",
            old_name="name",
            new_name="description",
        ),
        migrations.AlterField(
            model_name="product_arrival",
            name="date",
            field=models.DateField(
                blank=True, default=datetime.datetime(2024, 6, 19, 20, 53, 6, 572147)
            ),
        ),
    ]
