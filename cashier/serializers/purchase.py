"""Products serializer module."""
import pytz
from rest_framework import serializers

from cashier.models import Purchase
from cashier.serializers.purchase_detail import PurchaseDetailSerializer
from cashier.serializers.products import ProductSerializer

class PurchaseSerializer(serializers.ModelSerializer):
    """Purchase Serializer."""
    cashier = serializers.CharField(source='cashier.first_name', read_only=True)
    supplier = serializers.CharField(source='supplier.kode', read_only=True)
    supplier_id = serializers.CharField(source='supplier.id', read_only=True)
    purchase_invoice = PurchaseDetailSerializer(many=True)
    date = serializers.DateTimeField(required=False, read_only=True)
    # purchase_product = ProductSerializer(many=True)
    report_status = serializers.SerializerMethodField()
    report_payment_status = serializers.SerializerMethodField()

    class Meta:  # noqa D106
        model = Purchase
        name = 'purchase'
        fields = ('id', 'invoice', 'date', 'cashier', 'supplier', 'supplier_id', 'total', 'purchase_invoice', 'status', 'payment_status', 'report_status', 'report_payment_status')
        # fields = ('id', 'invoice', 'date', 'cashier', 'supplier', 'supplier_id', 'total', 'invoice_purchase', 'status', 'payment_status', 'purchase_product')
        datatables_always_serialize = ('id')


    def get_report_status(self, instance):
        return instance.status + 1

    def get_report_payment_status(self, instance):
        return instance.payment_status + 1