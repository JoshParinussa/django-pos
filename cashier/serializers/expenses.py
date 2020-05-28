"""Products serializer module."""
from rest_framework import serializers

from cashier.models import Expenses

class ExpensesSerializer(serializers.ModelSerializer):
    """Expenses Serializer."""
    cashier = serializers.CharField(source='cashier.username', read_only=True)

    class Meta:  # noqa D106
        model = Expenses
        name = 'expenses'
        fields = '__all__'
        datatables_always_serialize = ('id','date','cashier','information','cost')