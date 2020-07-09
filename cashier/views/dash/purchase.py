import logging
from datetime import date, datetime

import pytz
from pytz import timezone
from django.views.generic import TemplateView

from cashier.models import Purchase, PurchaseDetail, User, Supplier
from cashier.views.dash.base import DashListView, BaseUserPassesTestMixin, ManageBaseView
from cashier.services.supplier import supplier_services

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
            user = self.request.user
            today_invoice = datetime.now(timezone('Asia/Jakarta')).strftime("%d%m%Y")
            last_invoice = Purchase.objects.filter(created_at__startswith=date.today()).order_by('-created_at').first()
            if not last_invoice:
                count = 1
                invoice_number = 'B' + user.username.upper()[0] + str(user.id)[:5].upper() + today_invoice + str(count)
            else:
                count = int((last_invoice.invoice)[14:]) + 1
                invoice_number = 'B' + user.username.upper()[0] + str(user.id)[:5].upper() + today_invoice + str(count)
        
            context['invoice_number'] = invoice_number
        context['suppliers'] = supplier_services.get_suppliers_list()
        
        return context