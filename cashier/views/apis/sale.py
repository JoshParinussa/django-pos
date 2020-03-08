"""Product Api view."""
from cashier.models import Pembayaran
from cashier.serializers.sale import SaleSerializer
from rest_framework import viewsets


class SaleViewSet(viewsets.ModelViewSet):
    """ProductViewSet."""
    serializer_class = SaleSerializer
    queryset = Pembayaran.objects.order_by('created_at')
