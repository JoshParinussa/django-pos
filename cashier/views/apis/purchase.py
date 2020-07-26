"""Product Api view."""
import datetime

import pytz
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from cashier.models import Purchase
from cashier.serializers.purchase import PurchaseSerializer
from cashier.services.common import common_services


class PurchaseViewSet(viewsets.ModelViewSet):
    """PurchaseViewSet."""
    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.order_by('created_at')

    def get_queryset(self):
        date_range = self.request.GET.getlist('date_range[]')
        dates = common_services.convert_date_to_utc(date_range)
        queryset = Purchase.objects.all()
        if date_range:
            if self.request.user.is_superuser:
                queryset = queryset.filter(date__range=dates)
            else:
                queryset = queryset.filter(date__range=dates, cashier=self.request.user)
            
        return queryset

    @action(detail=False, methods=['POST'])
    def print_report(self, request):
        date_range = request.POST.getlist('date_range[]')
        dates = common_services.convert_date_to_utc(date_range)

        if date_range:
            queryset = self.queryset.filter(date__range=dates)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ReportPurchaseViewSet(viewsets.ModelViewSet):
    """ReportPurchaseViewSet."""
    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.order_by('created_at')

    @action(detail=False, methods=['POST'])
    def set_datatable(self, request):
        """set_datatable."""
        date_range = request.POST.getlist('date_range[]')
        payment_status = request.POST.get('payment_status')
        dates = common_services.convert_date_to_utc(date_range)
        queryset = Purchase.objects.all()
        if date_range:
            if payment_status:
                queryset = queryset.filter(date__range=dates, payment_status=payment_status)
            else:
                queryset = queryset.filter(date__range=dates)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

