"""Invoice serializer module."""
from rest_framework import serializers

from cashier.models import Invoice
from cashier.serializers.sale import SaleSerializer

class InvoiceSerializer(serializers.ModelSerializer):
    """Products Serializer."""
    cashier = serializers.CharField(source='cashier.first_name', read_only=True)
    invoice_sale = SaleSerializer(read_only=True, many=True)
    date = serializers.DateTimeField(format="%Y-%m-%d", required=False, read_only=True)
    class Meta:  # noqa D106
        model = Invoice
        name = 'invoice'
        fields = ('id', 'invoice', 'date', 'cashier', 'cash', 'change', 'total', 'status', 'invoice_sale')
