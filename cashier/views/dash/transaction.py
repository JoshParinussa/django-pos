from django.views.generic import TemplateView


class SaleTransactionView(TemplateView):
    """SaleTransactionView."""
    template_name = 'dash/transaction/sale.html'
