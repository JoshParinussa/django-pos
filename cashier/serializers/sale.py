"""Products serializer module."""
from rest_framework import serializers

from cashier.models import Pembayaran


class SaleSerializer(serializers.ModelSerializer):
    """Sale Serializer."""

    class Meta:  # noqa D106
        model = Pembayaran
        name = 'pembayaran'
        fields = '__all__'
