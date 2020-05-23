"""Invoice serializer module."""
from rest_framework import serializers

from cashier.models import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    """Products Serializer."""
    cashier = serializers.CharField(source='cashier.first_name', read_only=True)

    class Meta:  # noqa D106
        model = Invoice
        name = 'invoice'
        fields = '__all__'
