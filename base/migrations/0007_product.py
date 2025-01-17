# Generated by Django 4.2.17 on 2025-01-08 18:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_companyuser_is_archived'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True, max_length=200, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=10.0, max_digits=10, validators=[django.core.validators.MinValueValidator(1)])),
            ],
        ),
    ]
