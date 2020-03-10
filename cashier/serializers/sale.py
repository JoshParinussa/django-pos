"""Products serializer module."""
from rest_framework import serializers

from cashier.models import Sale


class SaleSerializer(serializers.ModelSerializer):
    """Sale Serializer."""

    class Meta:  # noqa D106
        model = Sale
        name = 'sale'
        fields = '__all__'
