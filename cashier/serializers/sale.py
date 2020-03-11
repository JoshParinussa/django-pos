"""Products serializer module."""
from rest_framework import serializers

from cashier.models import Sale


class SaleSerializer(serializers.ModelSerializer):
    """Sale Serializer."""
    barcode = serializers.CharField(source='product.barcode', read_only=True)
    product = serializers.CharField(source='product.name', read_only=True)
    price = serializers.CharField(source='product.selling_price', read_only=True)

    class Meta:  # noqa D106
        model = Sale
        name = 'sale'
        fields = ['id', 'barcode', 'invoice', 'product', 'price', 'qty', 'total']
        datatables_always_serialize = ('id', 'invoice', 'product', 'qty', 'total')
