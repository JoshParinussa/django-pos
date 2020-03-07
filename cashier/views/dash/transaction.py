from django.views.generic import TemplateView


class RegularTransactionView(TemplateView):
    """RegularTransactionView."""
    template_name = 'dash/transaction/regular.html'
