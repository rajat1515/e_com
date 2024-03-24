# Generated by Django 4.2.4 on 2024-03-24 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_rename_description_product_type_product_manufacturer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendoruser',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('supervisor', 'Supervisor'), ('salesperson', 'Salesperson'), ('customer', 'Customer')], max_length=50),
        ),
    ]
