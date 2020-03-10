"""Product Api view."""
from cashier.models import Pembayaran, Invoice, Product, Sale
from cashier.serializers.sale import SaleSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.forms.models import model_to_dict


class SaleViewSet(viewsets.ModelViewSet):
    """ProductViewSet."""
    serializer_class = SaleSerializer
    queryset = Pembayaran.objects.order_by('created_at')

    @action(detail=False, methods=['POST'])
    def add_item(self, request):
        """add_item."""
        invoice_number = request.POST.get('invoice_number')
        barcode = request.POST.get('barcode')
        qty = request.POST.get('qty')
        total = request.POST.get('total')

        invoice = Invoice.objects.get(invoice=invoice_number)
        product = Product.objects.get(barcode=barcode)

        save = Sale.objects.create(invoice=invoice, product=product, qty=qty, total=total)

        return Response(model_to_dict(save))


    @action(detail=False, methods=['POST'])
    def get_by_invoice(self, request):
        """get_by_invoice."""
        invoice_number = request.POST.get('invoice_number')
        barcode = request.POST.get('barcode')
        qty = request.POST.get('qty')
        total = request.POST.get('total')

        invoice = Invoice.objects.get(invoice=invoice_number)
        product = Product.objects.get(barcode=barcode)

        save = Sale.objects.create(invoice=invoice, product=product, qty=qty, total=total)

        return Response(model_to_dict(save))