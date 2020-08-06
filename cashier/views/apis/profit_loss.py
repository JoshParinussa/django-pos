"""Supplier Api view."""
from cashier.models import Invoice,Purchase,Income,Expense
from cashier.serializers.invoice import InvoiceSerializer
from cashier.serializers.purchase import PurchaseSerializer
from cashier.serializers.income import IncomeSerializer
from cashier.serializers.expense import ExpenseSerializer
from rest_framework import viewsets
from cashier.services.common import common_services
from rest_framework.decorators import action
from rest_framework.response import Response
from django.forms.models import model_to_dict

class ProfitLossViewSet(viewsets.ModelViewSet):
    """ProfitLossViewSet."""
    serializer_class = IncomeSerializer
    queryset = Income.objects.order_by('created_at')

    @action(detail=False, methods=['POST'])
    def set_datatable(self, request):
        """set_datatable."""
        date_range = request.POST.getlist('date_range[]')
        dates = common_services.convert_date_to_utc(date_range)
        invoices = Invoice.objects.filter(date__range=dates, status=1).only("date","total","member")
        purchases = Purchase.objects.filter(date__range=dates, payment_status=1).only("date","total","supplier")
        incomes = Income.objects.filter(date__range=dates).only("date","keterangan","jumlah_pemasukan")
        expenses = Expense.objects.filter(date__range=dates).only("date","information","cost")
        
        revenue = 0
        cost = 0
        profit = 0

        array_temp={}
        datasets=[]
        for invoice in invoices:
            revenue += invoice.total
            array_temp={
                'date':invoice.date,
                'info':"Penjualan ke "+str(invoice.member),
                'total':invoice.total
            }
            datasets.append(array_temp)
            array_temp={}
        for income in incomes:
            revenue += income.jumlah_pemasukan

        for purchase in purchases:
            cost += purchase.total

        for expense in expenses:
            cost += expense.cost

        profit = revenue - cost
        context = {}
        context['revenue'] = revenue
        context['cost'] = cost
        context['profit'] = profit

        return Response(context)
        
