# Generated by Django 4.2.14 on 2024-07-13 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('document', models.FileField(upload_to='documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='import_product_shipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reciever', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('quantity', models.IntegerField(default=0)),
                ('product_id', models.CharField(max_length=100)),
                ('billing_number', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Import_products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('description', models.TextField(blank=True)),
                ('gtd_id', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('category', models.CharField(max_length=100)),
                ('quantity', models.IntegerField(default=0)),
                ('income_quantity', models.IntegerField(default=0)),
                ('income_price', models.CharField(default=0, max_length=100)),
                ('minimal_price', models.CharField(default=0, max_length=100)),
            ],
            options={
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('income_price', models.CharField(default=0)),
                ('minimal_price', models.CharField(default=0)),
                ('category', models.CharField(default='Резцы', max_length=100)),
                ('quantity', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='product_arrival',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier', models.CharField(max_length=100)),
                ('date', models.DateField(blank=True)),
                ('quantity', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='product_shipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reciever', models.CharField(max_length=100)),
                ('date', models.DateField(blank=True)),
                ('quantity', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]
