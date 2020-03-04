"""Product Api view."""
from cashier.models import Product
from cashier.serializers.products import ProductSerializer
from rest_framework import viewsets


class ProductViewSet(viewsets.ModelViewSet):
    """ProductViewSet."""
    serializer_class = ProductSerializer
    queryset = Product.objects.order_by('created_at')
