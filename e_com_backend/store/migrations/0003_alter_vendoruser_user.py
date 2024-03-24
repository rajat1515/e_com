# Generated by Django 4.2.4 on 2024-03-24 09:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0002_rename_description_product_type_product_manufacturer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendoruser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='vendor_user', to=settings.AUTH_USER_MODEL),
        ),
    ]