"""Product Api view."""
from cashier.models import Invoice, Product, Sale
from cashier.serializers.sale import SaleSerializer, InvoiceSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.forms.models import model_to_dict
from django.http import HttpResponse

class SaleViewSet(viewsets.ModelViewSet):
    """ProductViewSet."""
    serializer_class = SaleSerializer
    queryset = Sale.objects.order_by('created_at')

    def get_price(self, product, newqty):
        """get_price."""
        harga_bertingkats = product.hargabertingkat.all().order_by('max_quantity')
        found = False
        if harga_bertingkats:
            for harga_bertingkat in harga_bertingkats:
                if harga_bertingkat.min_quantity <= newqty <= harga_bertingkat.max_quantity:
                    harga = harga_bertingkat.price
                    found = True
                    break
            if found is False:
                if newqty > harga_bertingkats.last().max_quantity:
                    harga = harga_bertingkats.last().price
                else:
                    harga = product.selling_price
                print("#MASUK", harga)
        else:
            harga = product.selling_price
        return harga

    @action(detail=False, methods=['POST'])
    def add_item(self, request):
        """add_item."""
        invoice_number = request.POST.get('invoice_number')
        barcode = request.POST.get('barcode')
        qty = request.POST.get('qty')
        invoice = Invoice.objects.get(invoice=invoice_number)
        product = Product.objects.get(barcode=barcode)
        harga_bertingkats = product.hargabertingkat.all() 
        
        try:
            product.stock = product.stock - int(qty)
            product.save(update_fields=["stock"])
        except Exception as e:
            print(e)

        try:
            sale_item = Sale.objects.get(invoice=invoice, product=product)
            new_qty = int(sale_item.qty) + int(qty)
            harga = self.get_price(product, new_qty)
            new_total = new_qty * harga
            sale_item.qty = new_qty
            sale_item.price = harga
            sale_item.total = new_total
            sale_item.save(update_fields=['qty', 'price', 'total'])
        except Exception as e:
            print(e)
            harga = self.get_price(product, int(qty))
            total = int(qty) * harga
            sale_item = Sale.objects.create(invoice=invoice, product=product, qty=qty, price=harga, total=total)
        
        context = {'sale': model_to_dict(sale_item),
                   'price': harga}

        return Response(context)

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
        new_qty = int(request.POST.get('qty'))
        new_total = request.POST.get('total')

        invoice = Invoice.objects.get(invoice=invoice_number)
        product = Product.objects.get(barcode=barcode)

        item = Sale.objects.get(invoice=invoice, product=product)
        harga = self.get_price(product, new_qty)
        item.qty = new_qty
        item.price = harga
        item.total = new_qty * harga
        item.save()
        return Response(model_to_dict(item))

class ReportTransactionViewSet(viewsets.ModelViewSet):
    """ReportTransactionViewSet."""
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.order_by('created_at')

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
        qty = request.POST.get('qty')

        invoice = Invoice.objects.get(id=invoice_number)
        product = Product.objects.get(barcode=barcode)
        product.stock += int(qty)
        product.save()

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
        diff_qty = request.POST.get('diffQty')

        invoice = Invoice.objects.get(id=invoice_number)
        product = Product.objects.get(barcode=barcode)
        product.stock += int(diff_qty)
        product.save()
        
        item = Sale.objects.get(invoice=invoice, product=product)
        item.qty = new_qty
        item.total = new_total
        item.save()

        invoice.total = grand_total
        invoice.cash = cash
        invoice.change = change
        invoice.save()

        return HttpResponse(status=201)