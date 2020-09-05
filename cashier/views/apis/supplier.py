"""Supplier Api view."""
from cashier.models import Supplier
from cashier.serializers.supplier import SupplierSerializer
from cashier.serializers.purchase import PurchaseSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from cashier.views.apis.base import APIBaseView
from cashier.services.common import common_services


class SupplierViewSet(viewsets.ModelViewSet):
    """SupplierViewSet."""
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.order_by('created_at')


class ReportSupplierViewSet(APIBaseView):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.order_by('kode')

    @action(detail=False, methods=['POST'])
    def set_datatable(self, request):
        """set_datatable."""
        supplier_pk = request.data['pk']

        date_range = request.POST.getlist('date_range[]')

        supplier = self.queryset.filter(id=supplier_pk).first()
        if date_range:
            dates = common_services.convert_date_to_utc(date_range)
            purchases = supplier.purchase_supplier.filter(date__range=dates)
        else:
            purchases = supplier.purchase_supplier.all()
        serializer = PurchaseSerializer(purchases, many=True)
        return Response(serializer.data)