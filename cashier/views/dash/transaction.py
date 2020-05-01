from django.views.generic import TemplateView
from cashier.models import Invoice, Sale, User
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

class ReportSaleView(DashListView):
    """ReportSaleView"""
    template_name = "dash/report/list_sale.html"
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
        object_cashier = User.objects.filter(id=object_invoice.cashier_id).first()
        context['date'] = object_invoice.date
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

class ReportProfitLossView(DashListView):
    template_name = "dash/report/profit_loss.html"
    model = Invoice