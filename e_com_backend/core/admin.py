from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from core.models import Vendor, Domain, User


@admin.register(Vendor)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ["schema_name"]



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('id', 'email', 'is_staff', 'date_joined', 'created_by')
    search_fields = ('email', 'name')
    readonly_fields = ('date_joined',)
