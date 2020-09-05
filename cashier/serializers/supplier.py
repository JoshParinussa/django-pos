"""Products serializer module."""
from rest_framework import serializers

from cashier.models import Supplier
from cashier.serializers.purchase import PurchaseSerializer

class SupplierSerializer(serializers.ModelSerializer):
    """Supplier Serializer."""
    # FILTER SERIALIZER
    # purchase_supplier = serializers.SerializerMethodField()
    purchase_supplier = PurchaseSerializer(many=True)

    class Meta:  # noqa D106
        model = Supplier
        name = 'supplier'
        fields = '__all__'
        datatables_always_serialize = ('id','company_name','address','contact_person','office_phone','phone', 'purchase_supplier')

    # def get_purchase_supplier(self, instance):
        # FILTER
        # purchase_supplier = instance.purchase_supplier.filter(status=1)
        # return PurchaseSerializer(purchase_supplier, many=True).data