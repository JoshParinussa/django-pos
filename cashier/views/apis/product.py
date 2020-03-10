"""Product Api view."""
from cashier.models import Product, ConvertBarang
from cashier.serializers.products import ProductSerializer, ConvertBarangSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class ProductViewSet(viewsets.ModelViewSet):
    """ProductViewSet."""
    serializer_class = ProductSerializer
    queryset = Product.objects.order_by('created_at')

    @action(detail=False, methods=['POST'])
    def get_by_barcode(self, request):
        """get_by_barcode."""
        barcode = request.POST.get('barcode')
        # product = Product.objects.get(barcode=barcode)
        queryset = self.get_queryset().filter(barcode=barcode)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ConvertViewSet(viewsets.ModelViewSet):
    """ConvertViewSet."""
    serializer_class = ConvertBarangSerializer
    queryset = ConvertBarang.objects.order_by('created_at')

    @action(detail=False, methods=['POST'])
    def get_by_product(self, request):
        """get_by_product."""
        product = request.POST.get('product')
        # product = Product.objects.get(barcode=barcode)
        queryset = self.get_queryset().filter(product=product)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
