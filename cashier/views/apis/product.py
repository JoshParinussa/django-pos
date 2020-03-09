"""Product Api view."""
from cashier.models import Product, ConvertBarang
from cashier.serializers.products import ProductSerializer, ConvertBarangSerializer
from rest_framework import viewsets


class ProductViewSet(viewsets.ModelViewSet):
    """ProductViewSet."""
    serializer_class = ProductSerializer
    queryset = Product.objects.order_by('created_at')

class ConvertViewSet(viewsets.ModelViewSet):
    """ConvertViewSet."""
    serializer_class = ConvertBarangSerializer
    queryset = Product.objects.order_by('created_at')
