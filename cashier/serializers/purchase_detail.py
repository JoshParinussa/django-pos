"""Products serializer module."""
from rest_framework import serializers

from cashier.models import Purchase, PurchaseDetail


class PurchaseDetailSerializer(serializers.ModelSerializer):
    """Purchase Serializer."""
    product = serializers.CharField(source='product.name', read_only=True)
    price   = serializers.CharField(source='product.purchase_price', read_only=True)
    invoice = serializers.CharField(source='invoice.invoice', read_only=True)

    class Meta:  # noqa D106
        model = PurchaseDetail
        name = 'purchasedetail'
        fields = ['id', 'invoice', 'product', 'price', 'qty', 'total']
        datatables_always_serialize = ('id', 'invoice', 'product', 'price', 'qty', 'total')
