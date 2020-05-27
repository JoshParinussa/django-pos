"""Products serializer module."""
from rest_framework import serializers

from cashier.models import Sale, Invoice


class SaleSerializer(serializers.ModelSerializer):
    """Sale Serializer."""
    barcode = serializers.CharField(source='product.barcode', read_only=True)
    product = serializers.CharField(source='product.name', read_only=True)
    price   = serializers.CharField(source='product.selling_price', read_only=True)
    invoice = serializers.CharField(source='invoice.invoice', read_only=True)

    class Meta:  # noqa D106
        model = Sale
        name = 'sale'
        fields = ['id', 'barcode', 'invoice', 'product', 'price', 'qty', 'total']
        datatables_always_serialize = ('id', 'invoice', 'product', 'price', 'qty', 'total')

class InvoiceSerializer(serializers.ModelSerializer):
    """Invoice Serialaizer."""
    cashier = serializers.CharField(source='cashier.username', read_only=True)
    date = serializers.DateTimeField(format="%Y-%m-%d", required=False, read_only=True)
    
    class Meta:  # noqa D106
        model = Invoice
        name = 'invoice'
        fields = '__all__'