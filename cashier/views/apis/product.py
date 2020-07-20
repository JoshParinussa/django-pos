"""Product Api view."""
from django.db.models import F
from cashier.models import Product, ConvertBarang
from cashier.serializers.products import ProductSerializer, ConvertBarangSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import django_filters
from cashier.views.apis.base import APIBaseView


class ProductViewSet(APIBaseView):
    """ProductViewSet."""
    serializer_class = ProductSerializer
    queryset = Product.objects.order_by('name')
    # filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)

    def get_queryset(self):
        queryset = Product.objects.all()
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
    
class ReportOutOfStockViewSet(APIBaseView):
    serializer_class = ProductSerializer
    queryset = Product.objects.order_by('name')

    def get_queryset(self):
        queryset = Product.objects.all()
        product_name = self.request.query_params.get('q', None)
        if product_name is not None:
            queryset = queryset.filter(name__icontains=product_name)
        return queryset

    ## REMOVE IF NOT USE
    # @action(detail=False, methods=['GET'])
    # def set_datatable(self, request):
    #     """set_datatable"""
    #     queryset = self.get_queryset().exclude(stock__gt=F('minimal_stock'))
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
