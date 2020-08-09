"""Supplier Api view."""
from cashier.models import Expense
from cashier.serializers.expense import ExpenseSerializer
from rest_framework import viewsets


class ExpenseViewSet(viewsets.ModelViewSet):
    """ExpenseViewSet."""
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.order_by('created_at')