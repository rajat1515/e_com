from django.db import models
from core.models import User


class VendorUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    USER_ROLES = (
        ('admin', 'Admin'),
        ('supervisor', 'Supervisor'),
        ('salesperson', 'Salesperson'),
        ('customer', 'Customer'),

    )
    role = models.CharField(max_length=50, choices=USER_ROLES)

    def __str__(self) -> str:
        return self.user.email + ' ' + self.role


class Store(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    contact_details = models.CharField(max_length=255)
    added_by = models.ForeignKey(VendorUser, null=True,
                                 related_name="stores_added",
                                 blank=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(VendorUser, null=True,
                                   related_name="stores_updated",
                                   blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Product(models.Model):
    store = models.ForeignKey(Store,
                              related_name='products',
                              on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    type = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    units = models.PositiveBigIntegerField(default=1)
    added_by = models.ForeignKey(VendorUser, null=True,
                                 related_name="products_added",
                                 blank=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(VendorUser, null=True,
                                   related_name="products_updated",
                                   blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProductSold(models.Model):
    sold_by = models.ForeignKey(VendorUser, related_name="products_sold",
                                null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, related_name="product",
                                null=True, on_delete=models.SET_NULL)
    unit_sold = models.PositiveBigIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
