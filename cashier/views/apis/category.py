"""Product Api view."""
from cashier.models import ProductCategory
from cashier.serializers.category import ProductCategorySerializer
from rest_framework import viewsets


class ProductCategoryViewSet(viewsets.ModelViewSet):
    """ProductCategoryViewSet."""
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.order_by('created_at')
