from rest_framework import serializers
from store.models import VendorUser, Store, Product, ProductSold
from core.models import User
from django.db import transaction
from re import match


class VendorUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.CharField(write_only=True)

    class Meta:
        model = VendorUser
        fields = ['email', 'role', 'password']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = instance.id
        data["email"] = instance.user.email
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        role = validated_data.pop('role')
        with transaction.atomic():
            user = User.objects.create_user(email=email, password=password)
            return VendorUser.objects.create(user=user, role=role)


class StoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Store
        fields = ['id', 'name',
                  'location', 'contact_details',
                  'created_at', 'updated_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        added_by = instance.added_by.user.email if instance.added_by else None
        ud_by = instance.updated_by.user.email if instance.updated_by else None
        data['added_by'] = added_by
        data['updated_by'] = ud_by
        return data


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['store', 'name', 'type', 'manufacturer', 'price', 'units']


class ProductSoldSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSold
        fields = ['product', 'unit_sold']

    def create(self, validated_data):
        product = validated_data.get('product')
        unit_sold = validated_data.get('unit_sold')
        vendor_user = self.context.get('vendor_user')

        if not (product and unit_sold):
            raise serializers.ValidationError("product and unit_sold is required.")

        with transaction.atomic():

            if unit_sold > product.units:
                raise serializers.ValidationError("Quantity sold cannot \
                                                  exceed available quantity.")

            product_sold = ProductSold.objects.create(
                product=product,
                unit_sold=unit_sold,
                sold_by=vendor_user
            )

            # Decrease product quantity
            product.units -= unit_sold
            product.save()

        return product_sold


class CustomerRegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    email = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)

    class Meta:
        model = VendorUser
        fields = ['first_name', 'last_name', 'email', 'password']

    def validate_first_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("First name must contain only alphabets.")
        return value

    def validate_last_name(self, value):
        if not match(r'^[a-zA-Z.\']+$', value):
            raise serializers.ValidationError("Last name must contain only alphabets, a dot, or a single quote.")
        return value

    def validate_password(self, value):
        if not match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,12}$', value):
            raise serializers.ValidationError("Password must be 8-12 \
                                              characters long and contain \
                                              at least one uppercase letter, \
                                              one lowercase letter, one digit,\
                                              and one special character.")
        return value

    def validate(self, data):
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists.")
        return data

    def create(self, validated_data):
        email = validated_data.pop('email')
        with transaction.atomic():
            user = User.objects.create_user(email=email, **validated_data)
            return VendorUser.objects.create(user=user, role="customer")
