"""Products serializer module."""
from rest_framework import serializers

from cashier.models import ProductCategory


class ProductCategorySerializer(serializers.ModelSerializer):
    """Products Serializer."""

    class Meta:  # noqa D106
        model = ProductCategory
        name = 'product_category'
        fields = '__all__'
        datatables_always_serialize = ('id')
