from django.views.generic import TemplateView
from cashier.models import Invoice
from datetime import datetime, date
from cashier.views.dash.base import DashListView


class SaleTransactionView(TemplateView):
    """SaleTransactionView."""
    template_name = 'dash/transaction/sale.html'

    def get_context_data(self, **kwargs):
        """Override get context."""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        today_invoice = datetime.now().date().strftime("%d%m%Y")
        last_invoice = Invoice.objects.filter(created_at__startswith=date.today()).order_by('-created_at').first()
        if not last_invoice:
            count = 1
            invoice_number = 'K' + user.username.upper()[0] + today_invoice + str(count)
            Invoice.objects.create(invoice=invoice_number, cashier=user)
        else:
            if last_invoice.status == 1 or last_invoice.status == 2:
                count = int((last_invoice.invoice)[10:]) + 1
                invoice_number = 'K' + user.username.upper()[0] + today_invoice + str(count)
                Invoice.objects.create(invoice=invoice_number, cashier=user)
            else:
                invoice_number = last_invoice.invoice

        context['invoice_number'] = invoice_number

        return context

class ReportTransactionView(DashListView):
    """ReportTransactionView"""
    template_name = "dash/report/list_transaction.html"
    model = Invoice
    

