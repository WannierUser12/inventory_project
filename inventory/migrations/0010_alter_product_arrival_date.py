# Generated by Django 5.0.4 on 2024-05-18 17:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0009_alter_product_category_alter_product_arrival_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product_arrival",
            name="date",
            field=models.DateField(
                blank=True, default=datetime.datetime(2024, 5, 18, 22, 48, 27, 964152)
            ),
        ),
    ]
