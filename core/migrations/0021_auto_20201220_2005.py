# Generated by Django 3.1.2 on 2020-12-20 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20201220_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellproduct',
            name='product_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sellproducts', to='core.stock'),
        ),
    ]
