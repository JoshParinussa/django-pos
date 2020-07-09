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
        date_range = ['2020-07-10', '2020-07-10']
        dates = common_services.convert_date_to_utc(date_range)
        
        if date_range:
            queryset = self.queryset.filter(date__range=dates, cashier=self.request.user, total__isnull=False)
            
        return queryset

    @action(detail=False, methods=['POST'])
    def print_report(self, request):
        date_range = request.POST.getlist('date_range[]')
        dates = common_services.convert_date_to_utc(date_range)

        if date_range:
            queryset = self.queryset.filter(date__range=dates)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)