"""Supplier Api view."""
from cashier.models import Supplier
from cashier.serializers.supplier import SupplierSerializer
from rest_framework import viewsets


class SupplierViewSet(viewsets.ModelViewSet):
    """SupplierViewSet."""
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.order_by('created_at')