"""Expense serializer module."""
from rest_framework import serializers

from cashier.models import Expense

class ExpenseSerializer(serializers.ModelSerializer):
    """Expense Serializer."""
    cashier = serializers.CharField(source='cashier.username', read_only=True)

    class Meta:  # noqa D106
        model = Expense
        name = 'expenses'
        fields = '__all__'
        datatables_always_serialize = ('id','date','cashier','information','cost')