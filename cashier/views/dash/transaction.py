import logging
from datetime import date, datetime

import pytz
from pytz import timezone
from django.views.generic import TemplateView

from cashier.models import Invoice, Sale, User
from cashier.views.dash.base import DashListView, BaseUserPassesTestMixin, ManageBaseView
from cashier.services.member import member_services
from cashier.services.code_generator import code_generator

logger = logging.getLogger(__name__)

class SaleTransactionListView(DashListView):
    """BrandListView."""
    template_name = 'dash/transaction/list.html'
    model = Invoice



class SaleTransactionView(ManageBaseView, TemplateView):
    """SaleTransactionView."""
    template_name = 'dash/transaction/sale.html'

    def get_context_data(self, **kwargs):
        """Override get context."""
        context = super().get_context_data(**kwargs)
        try:
            invoice_id = self.kwargs['pk']
            invoice = Invoice.objects.get(id=invoice_id)
            context['invoice_number'] = invoice.invoice
            context['invoice_status'] = invoice.status
            print("# STATUS", invoice.status)
        except Exception as e:
            logger.error(e)
            context['invoice_number'] = code_generator.generate(self.request.user, Invoice)
        context['members'] = member_services.get_members_list()
        
        return context

class ReportTransactionView(DashListView, BaseUserPassesTestMixin):
    """ReportTransactionView"""
    template_name = "dash/report/list_transaction.html"
    model = Invoice

class ReportSaleView(DashListView, BaseUserPassesTestMixin):
    """ReportSaleView"""
    template_name = "dash/report/list_sale_2.html"
    model = Sale

    def get_context_data(self, **kwargs):
        """Override get context."""
        model = self.get_model()
        context = super().get_context_data(**kwargs)
        context['model_name'] = model._meta.verbose_name.title()
        context['model_name_plural'] = model._meta.verbose_name_plural.title()
        context['icon'] = self.get_icon()
        context['action'] = self.get_current_action()
        object_invoice = Invoice.objects.filter(id=self.kwargs.get('pk')).first()
        if(object_invoice.total == None):
            object_invoice.total = 0

        if(object_invoice.cash == None):
            object_invoice.cash = 0

        if(object_invoice.change == None):
            object_invoice.change = 0
        
        object_cashier = User.objects.filter(id=object_invoice.cashier_id).first()
        context['date'] = object_invoice.date
        context['tanggal'] = object_invoice.date
        context['invoice_number'] = object_invoice.invoice
        context['invoice_total'] = object_invoice.total
        context['invoice_cash'] = object_invoice.cash
        context['invoice_change'] = object_invoice.change
        context['cashier'] = object_cashier.username
        context['invoice_id'] = self.kwargs.get('pk')

        for action in self.get_actions():
            url_name = self._get_url_name(action)
            context[f'{action}_url_name'] = url_name

        return context

class ReportSalebyProductView(DashListView, BaseUserPassesTestMixin):
    """ReportSaleView"""
    template_name = "dash/report/list_sale_by_product.html"
    model = Sale

    def get_context_data(self, **kwargs):
        """Override get context."""
        model = self.get_model()
        context = super().get_context_data(**kwargs)
        context['model_name'] = model._meta.verbose_name.title()
        context['model_name_plural'] = model._meta.verbose_name_plural.title()
        context['icon'] = self.get_icon()
        context['action'] = self.get_current_action()
        for action in self.get_actions():
            url_name = self._get_url_name(action)
            context[f'{action}_url_name'] = url_name

        return context