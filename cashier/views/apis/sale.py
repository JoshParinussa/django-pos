"""Product Api view."""
from cashier.models import Invoice, Product, Sale
from cashier.serializers.sale import SaleSerializer, InvoiceSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.forms.models import model_to_dict
from django.http import HttpResponse
from datetime import datetime

class SaleViewSet(viewsets.ModelViewSet):
    """ProductViewSet."""
    serializer_class = SaleSerializer
    queryset = Sale.objects.order_by('created_at')

    @action(detail=False, methods=['POST'])
    def add_item(self, request):
        """add_item."""
        invoice_number = request.POST.get('invoice_number')
        barcode = request.POST.get('barcode')
        qty = request.POST.get('qty')
        total = request.POST.get('total')
        invoice = Invoice.objects.get(invoice=invoice_number)
        product = Product.objects.get(barcode=barcode)

        try:
            product.stock = product.stock - int(qty)
            product.save(update_fields=["stock"])
        except Exception as e:
            print(e)

        try:
            sale_item = Sale.objects.get(invoice=invoice, product=product)
            new_qty = int(sale_item.qty) + int(qty)
            new_total = int(sale_item.total) + int(total)
            sale_item.qty = new_qty
            sale_item.total = new_total
            sale_item.save(update_fields=['qty', 'total'])
        except Exception as e:
            print(e)
            sale_item = Sale.objects.create(invoice=invoice, product=product, qty=qty, total=total)

        return Response(model_to_dict(sale_item))

    @action(detail=False, methods=['POST'])
    def get_by_invoice(self, request):
        """get_by_invoice."""
        invoice_number = request.POST.get('invoice_number')
        invoice = Invoice.objects.get(invoice=invoice_number)
        queryset = self.get_queryset().filter(invoice=invoice)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def process_payment(self, request):
        """get_by_invoice."""
        invoice_number = request.POST.get('invoice_number')
        cash = request.POST.get('cash')
        change = request.POST.get('change')
        total = request.POST.get('total')

        invoice = Invoice.objects.get(invoice=invoice_number)
        invoice.cash = cash
        invoice.change = change
        invoice.total = total
        invoice.status = 1
        invoice.cashier = self.request.user
        invoice.save(update_fields=["cash", "cashier", "change", "total", "status"])

        return HttpResponse(status=202)

    @action(detail=False, methods=['POST'])
    def delete_item(self, request):
        """delete_item."""
        invoice_number = request.POST.get('invoice_number')
        barcode = request.POST.get('barcode')

        invoice = Invoice.objects.get(invoice=invoice_number)
        product = Product.objects.get(barcode=barcode)

        item = Sale.objects.get(invoice=invoice, product=product)
        item.delete()
        return Response(model_to_dict(item))

    @action(detail=False, methods=['POST'])
    def update_item(self, request):
        """update_item."""
        invoice_number = request.POST.get('invoice_number')
        barcode = request.POST.get('barcode')
        new_qty = request.POST.get('qty')
        new_total = request.POST.get('total')

        invoice = Invoice.objects.get(invoice=invoice_number)
        product = Product.objects.get(barcode=barcode)

        item = Sale.objects.get(invoice=invoice, product=product)
        item.qty = new_qty
        item.total = new_total
        item.save()
        return Response(model_to_dict(item))

class ReportTransactionViewSet(viewsets.ModelViewSet):
    """ReportTransactionViewSet."""
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.order_by('created_at')

    @action(detail=False, methods=['POST'])
    def set_datatable(self, request):
        """set_datatable."""
        condition = request.POST.get('date')
        if condition == '1':
            date_condition = datetime.now().date()
            queryset = self.get_queryset().filter(date__gte=date_condition)
        elif condition == '2':
            date_condition = datetime.now().month
            queryset = self.get_queryset().filter(date__month=date_condition)
        elif condition == '3':
            date_condition = datetime.now().year
            queryset = self.get_queryset().filter(date__year=date_condition)
        elif condition == '4' :
            queryset = self.get_queryset()
        else :
            queryset = ''
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def set_income(self, request):
        """set_income."""
        condition = request.POST.get('date')
        if condition == '1':
            date_condition = datetime.now().date()
            data = Invoice.objects.all().filter(date__gte=date_condition)
        elif condition == '2':
            date_condition = datetime.now().month
            data = Invoice.objects.all().filter(date__month=date_condition)
        elif condition == '3':
            date_condition = datetime.now().year
            data = Invoice.objects.all().filter(date__year=date_condition)
        else :
            data = Invoice.objects.all()
        
        income = 0
        for e in data:
            if  e.total == None :
                e.total = 0
            income += e.total
        
        context={}
        context['income'] = income
        context['date'] = datetime.now().date()

        return Response(context)
    


class ReportSaleViewSet(viewsets.ModelViewSet):
    """ReportSaleViewSet."""
    serializer_class = SaleSerializer
    queryset = Sale.objects.order_by('created_at')

    @action(detail=False, methods=['POST'])
    def get_by_invoice(self, request):
        """get_by_invoice."""
        invoice_id = request.POST.get('invoice')
        queryset = self.get_queryset().filter(invoice_id=invoice_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def delete_item(self, request):
        """delete_item."""
        invoice_number = request.POST.get('invoice_number')
        barcode = request.POST.get('barcode')
        total = request.POST.get('total')
        change = request.POST.get('change')

        invoice = Invoice.objects.get(id=invoice_number)
        product = Product.objects.get(barcode=barcode)

        item = Sale.objects.get(invoice=invoice, product=product)
        item.delete()

        invoice.total = total
        invoice.change = change
        invoice.save()

        return HttpResponse(status=201)

    @action(detail=False, methods=['POST'])
    def update_item(self, request):
        """update_item."""
        invoice_number = request.POST.get('invoice_number')
        barcode = request.POST.get('barcode')
        new_qty = request.POST.get('qty')
        new_total = request.POST.get('total')
        grand_total = request.POST.get('grand_total')
        cash = request.POST.get('cash')
        change = request.POST.get('change')

        invoice = Invoice.objects.get(id=invoice_number)
        product = Product.objects.get(barcode=barcode)
        
        item = Sale.objects.get(invoice=invoice, product=product)
        item.qty = new_qty
        item.total = new_total
        item.save()

        invoice.total = grand_total
        invoice.cash = cash
        invoice.change = change
        invoice.save()

        return HttpResponse(status=201)