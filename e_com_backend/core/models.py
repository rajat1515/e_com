from django.db import models
from django.core.exceptions import ValidationError
from django_tenants.models import TenantMixin, DomainMixin
from re import match
from django.contrib.auth.models import (AbstractBaseUser,
                                        PermissionsMixin,
                                        BaseUserManager)
from django.utils import timezone


def validate_pan_number(value):
    if not match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', value):
        raise ValidationError('Invalid PAN number. PAN number should be in the format: ABCDE1234F')


class Vendor(TenantMixin):
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    gst = models.CharField(max_length=15, unique=True)
    pan = models.CharField(max_length=10, unique=True,
                           validators=[validate_pan_number])

    def __str__(self):
        return self.schema_name


class Domain(DomainMixin):
    pass


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('email not present')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=150, blank=True, default="")
    last_name = models.CharField(max_length=150, blank=True, default="")
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey('self', null=True, blank=True,
                                   on_delete=models.SET_NULL)
    objects = UserManager()
    USERNAME_FIELD = "email"
