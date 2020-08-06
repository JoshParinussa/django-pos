import logging
from datetime import date, datetime

import pytz
from pytz import timezone
from django.views.generic import TemplateView

from cashier.models import Invoice, Purchase, Income, Expense
from cashier.views.dash.base import DashListView, BaseUserPassesTestMixin, ManageBaseView
from cashier.services.member import member_services
from cashier.services.common import common_services

class ReportProfitLossView(DashListView, BaseUserPassesTestMixin):
    template_name = "dash/report/profit_loss.html"
    model = Invoice

    def get_context_data(self, **kwargs):
        """Override get context."""
        context = super().get_context_data(**kwargs)
        date_range=[str(date.today()),str(date.today())]
        dates = common_services.convert_date_to_utc(date_range)
        invoices = Invoice.objects.filter(date__range=dates, status=1).only("date","total","member")
        purchases = Purchase.objects.filter(date__range=dates, payment_status=1).only("date","total","supplier")
        incomes = Income.objects.filter(date__range=dates).only("date","keterangan","jumlah_pemasukan")
        expenses = Expense.objects.filter(date__range=dates).only("date","information","cost")

        revenue = 0
        cost = 0
        profit = 0

        for invoice in invoices:
            revenue += invoice.total

        for income in incomes:
            revenue += income.jumlah_pemasukan
            
        for purchase in purchases:
            cost += purchase.total

        for expense in expenses:
            cost += expense.cost 
            
        profit = revenue - cost

        context['revenue'] = revenue
        context['profit'] = profit
        context['cost'] = cost

        return context