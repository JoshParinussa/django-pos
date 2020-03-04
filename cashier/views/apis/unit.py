"""Product Api view."""
from cashier.models import Unit
from cashier.serializers.unit import UnitSerializer
from rest_framework import viewsets


class UnitViewSet(viewsets.ModelViewSet):
    """UnitViewSet."""
    serializer_class = UnitSerializer
    queryset = Unit.objects.order_by('created_at')
