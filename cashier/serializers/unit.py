"""Products serializer module."""
from rest_framework import serializers

from cashier.models import Unit


class UnitSerializer(serializers.ModelSerializer):
    """Unit Serializer."""

    class Meta:  # noqa D106
        model = Unit
        name = 'unit'
        fields = '__all__'
