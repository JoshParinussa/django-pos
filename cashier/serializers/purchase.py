"""Products serializer module."""
import pytz
from rest_framework import serializers

from cashier.models import Purchase
from cashier.serializers.purchase_detail import PurchaseDetailSerializer


class PurchaseSerializer(serializers.ModelSerializer):
    """Purchase Serializer."""
    cashier = serializers.CharField(source='cashier.first_name', read_only=True)
    invoice_purchase = PurchaseDetailSerializer(read_only=True, many=True)
    date = serializers.DateTimeField(required=False, read_only=True)

    class Meta:  # noqa D106
        model = Purchase
        name = 'purchase'
        fields = ('id', 'invoice', 'date', 'cashier', 'supplier', 'total', 'invoice_purchase')
