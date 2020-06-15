"""Supplier Api view."""
from cashier.models import Income
from cashier.serializers.income import IncomeSerializer
from rest_framework import viewsets


class IncomeViewSet(viewsets.ModelViewSet):
    """IncomeViewSet."""
    serializer_class = IncomeSerializer
    queryset = Income.objects.order_by('created_at')