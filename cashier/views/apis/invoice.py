"""Product Api view."""
import datetime

import pytz
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from cashier.models import Invoice
from cashier.serializers.invoice import InvoiceSerializer
from cashier.services.common import common_services


class InvoiceViewSet(viewsets.ModelViewSet):
    """ProductViewSet."""
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.order_by('created_at')

    def get_queryset(self):
        date_range = self.request.GET.getlist('date_range[]')
        dates = common_services.convert_date_to_utc(date_range)
        
        if date_range:
            queryset = self.queryset.filter(date__range=dates, cashier=self.request.user)
            
        return queryset

    @action(detail=False, methods=['POST'])
    def print_report(self, request):
        date_range = request.POST.getlist('date_range[]')
        dates = common_services.convert_date_to_utc(date_range)

        if date_range:
            queryset = self.queryset.filter(date__range=dates)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
