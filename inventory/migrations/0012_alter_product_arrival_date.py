# Generated by Django 5.0.4 on 2024-05-18 18:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0011_alter_product_arrival_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product_arrival",
            name="date",
            field=models.DateField(
                blank=True, default=datetime.datetime(2024, 5, 18, 23, 16, 2, 925870)
            ),
        ),
    ]
