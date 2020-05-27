"""Product Api view."""
from cashier.models import Invoice
from cashier.serializers.invoice import InvoiceSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import datetime
from django.utils import timezone
import pytz


class InvoiceViewSet(viewsets.ModelViewSet):
    """ProductViewSet."""
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.order_by('created_at')

    @action(detail=False, methods=['POST'])
    def print_report(self, request):
        date_range = request.POST.getlist('date_range[]')
        date_format = '%Y-%m-%d'
        
        unaware_start_date = datetime.datetime.strptime(date_range[0], date_format)
        aware_start_date = pytz.utc.localize(unaware_start_date)

        unaware_end_date = datetime.datetime.strptime(date_range[1], date_format)
        aware_end_date = pytz.utc.localize(unaware_end_date)
        print_result = []

        if date_range:
            self.queryset = self.get_queryset().filter(date__range=(aware_start_date, datetime.datetime.combine(aware_end_date, datetime.time.max)))
            
        serializer = self.get_serializer(self.queryset, many=True)
        print("#DATE", serializer.data)
        return Response(serializer.data)