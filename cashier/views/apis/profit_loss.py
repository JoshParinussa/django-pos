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
        
        array_temp={}
        datasets=[]
        context = {}
        return Response(context)
        
    @action(detail=False, methods=['POST'])
    def set_profit_loss(self, request):
        date_range = request.POST.getlist('date_range[]')
        dates = common_services.convert_date_to_utc(date_range)
        invoices = Invoice.objects.filter(date__range=dates, status=1).only("date","total","member")
        purchases = Purchase.objects.filter(date__range=dates, payment_status=1).only("date","total","supplier")
        incomes = Income.objects.filter(date__range=dates).only("date","keterangan","jumlah_pemasukan")
        expenses = Expense.objects.filter(date__range=dates).only("date","information","cost")
        
        revenue = 0
        cost = 0
        profit = 0
        revenue_1 = 0
        revenue_2 = 0
        cost_1 = 0
        cost_2 = 0

        for invoice in invoices:
            if invoice.total == None :
                invoice.total = 0
            revenue += int(invoice.total)
            revenue_1 += int(invoice.total)

        for income in incomes:
            if income.jumlah_pemasukan == None:
                income.jumlah_pemasukan = 0
            revenue += int(income.jumlah_pemasukan)
            revenue_2 += int(income.jumlah_pemasukan)

        for purchase in purchases:
            if purchase.total == None :
                purchase.total = 0
            cost += int(purchase.total)
            cost_1 += int(purchase.total)

        for expense in expenses:
            if expense.cost == None :
                expense.cost = 0
            cost += int(expense.cost)
            cost_2 += int(expense.cost)

        profit = revenue - cost
        context = {}
        context['revenue'] = revenue
        context['revenue_1'] = revenue_1
        context['revenue_2'] = revenue_2
        context['cost'] = cost
        context['cost_1'] = cost_1
        context['cost_2'] = cost_2
        context['profit'] = profit

        return Response(context)
