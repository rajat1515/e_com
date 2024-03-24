from rest_framework import serializers
from core.models import Vendor, Domain


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

    def create(self, validated_data):
        schema_name = validated_data['schema_name']
        domain_name = f"{schema_name}.localhost"
        vn = Vendor.objects.create(**validated_data)
        Domain.objects.create(domain=domain_name, tenant=vn)
        return vn
