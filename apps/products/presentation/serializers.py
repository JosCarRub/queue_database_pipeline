from rest_framework import serializers
from decimal import Decimal

class CreateProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False,allow_blank=True, default='')
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.00'))