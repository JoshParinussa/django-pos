"""Products serializer module."""
from rest_framework import serializers

from cashier.models import Supplier

class SupplierSerializer(serializers.ModelSerializer):
    """Supplier Serializer."""

    class Meta:  # noqa D106
        model = Supplier
        name = 'supplier'
        fields = '__all__'
        datatables_always_serialize = ('id','company_name','address','contact_person','office_phone','phone')