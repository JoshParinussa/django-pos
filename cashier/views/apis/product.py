"""Product Api view."""
from cashier.models import Product, ConvertBarang
from cashier.serializers.products import ProductSerializer, ConvertBarangSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import django_filters


class ProductViewSet(viewsets.ModelViewSet):
    """ProductViewSet."""
    serializer_class = ProductSerializer
    queryset = Product.objects.order_by('created_at')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)

    def get_queryset(self):
        queryset = self.queryset
        product_name = self.request.query_params.get('q', None)
        if product_name is not None:
            queryset = queryset.filter(name__icontains=product_name)
        return queryset


    @action(detail=False, methods=['POST'])
    def get_by_barcode(self, request):
        """get_by_barcode."""
        barcode = request.POST.get('barcode')
        queryset = self.get_queryset().filter(barcode=barcode)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def get_by_name(self, request):
        """get_by_name."""
        id = request.POST.get('id')
        if id is not None:
            queryset = self.get_queryset().filter(id=id)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def get_product_select2(self, request):
        """get_by_barcode."""
        queryset = Product.objects.order_by('created_at').defer('id', 'name', 'barcode')
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
        queryset = self.get_queryset().filter(product=product)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
