"""Products serializer module."""
from rest_framework import serializers

from cashier.models import Sale, Invoice

from cashier.services.products import product_services


class SaleSerializer(serializers.ModelSerializer):
    """Sale Serializer."""
    barcode = serializers.CharField(source='product.barcode', read_only=True)
    product = serializers.CharField(source='product.name', read_only=True)
    price   = serializers.SerializerMethodField()
    invoice = serializers.CharField(source='invoice.invoice', read_only=True)


    def get_price(self, obj):
        price = product_services.get_harga_bertingkat(obj.product, obj.qty)
        return price
    class Meta:  # noqa D106
        model = Sale
        name = 'sale'
        fields = ['id', 'barcode', 'invoice', 'product', 'price', 'qty', 'total']
        datatables_always_serialize = ('id', 'invoice', 'product', 'price', 'qty', 'total')
