import logging
from datetime import date, datetime

import pytz
from pytz import timezone
from django.views.generic import TemplateView

from cashier.models import Purchase, PurchaseDetail, User, Supplier
from cashier.views.dash.base import DashListView, BaseUserPassesTestMixin, ManageBaseView
from cashier.services.supplier import supplier_services
from cashier.services.code_generator import code_generator

logger = logging.getLogger(__name__)

class PurchaseListView(DashListView):
    """PurchaseListView."""
    template_name = 'dash/purchase/list.html'
    model = Purchase

class PurchaseDetailView(ManageBaseView, TemplateView):
    """PurchaseDetailView."""
    template_name = 'dash/purchase/purchase.html'

    def get_context_data(self, **kwargs):
        """Override get context."""
        context = super().get_context_data(**kwargs)
        try:
            invoice_id = self.kwargs['pk']
            invoice = Purchase.objects.get(id=invoice_id)
            context['invoice_number'] = invoice.invoice
        except Exception as e:
            logger.error(e)
            context['invoice_number'] = code_generator.generate(self.request.user, Purchase)
        context['suppliers'] = supplier_services.get_suppliers_list()
        
        return context

class ReportPurchaseView(DashListView):
    """ReportPurchaseView."""
    template_name = 'dash/report/purchase.html'
    model = Purchase