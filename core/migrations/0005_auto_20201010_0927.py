# Generated by Django 3.1.2 on 2020-10-10 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20201009_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='office',
            name='name',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='office',
            name='phone',
            field=models.CharField(blank=True, max_length=11, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='purchaseproduct',
            name='product_name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='sellproduct',
            name='customer_name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='sellproduct',
            name='customer_phone',
            field=models.CharField(max_length=11),
        ),
        migrations.AlterField(
            model_name='stock',
            name='product_name',
            field=models.CharField(max_length=30),
        ),
    ]
