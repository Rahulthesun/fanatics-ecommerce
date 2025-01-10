# Generated by Django 4.2.17 on 2025-01-09 12:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_alter_cartitem_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='cart_total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]