# Generated by Django 4.2.17 on 2025-01-08 17:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0002_alter_companyuser_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companyuser',
            name='id',
        ),
        migrations.AlterField(
            model_name='companyuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
