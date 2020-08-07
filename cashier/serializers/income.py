"""Income serializer module."""
from rest_framework import serializers

from cashier.models import Income

class IncomeSerializer(serializers.ModelSerializer):
    """Income Serializer."""
    cashier = serializers.CharField(source='cashier.username', read_only=True)

    class Meta:  # noqa D106
        model = Income
        name = 'income'
        fields = '__all__'
        datatables_always_serialize = ('id')