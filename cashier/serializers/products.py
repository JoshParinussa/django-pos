"""Products serializer module."""
from rest_framework import serializers

from cashier.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """Products Serializer."""
    category = serializers.CharField(source='category.name', read_only=True)
    unit = serializers.CharField(source='unit.name', read_only=True)

    class Meta:  # noqa D106
        model = Product
        name = 'product'
        fields = '__all__'
