from django.contrib import admin
from .models import VendorUser, Store, Product, ProductSold


@admin.register(VendorUser)
class VendorUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role')


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'contact_details',
                    'added_by', 'updated_by', 'created_at', 'updated_at')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'store', 'units', 'price', 'added_by',
                    'updated_by', 'created_at', 'updated_at')


@admin.register(ProductSold)
class ProductSoldAdmin(admin.ModelAdmin):
    list_display = ['sold_by', 'product', 'unit_sold', 'created_at']
    search_fields = ['sold_by__user__email', 'product__name']
    list_filter = ['created_at']
