"""Supplier Api view."""
from cashier.models import Expenses
from cashier.serializers.expenses import ExpensesSerializer
from rest_framework import viewsets


class ExpensesViewSet(viewsets.ModelViewSet):
    """ExpensesViewSet."""
    serializer_class = ExpensesSerializer
    queryset = Expenses.objects.order_by('created_at')