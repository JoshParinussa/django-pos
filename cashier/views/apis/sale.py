"""Product Api view."""
# from datetime import datetime
import datetime

import pytz
from django.db.models import (Count, DecimalField, ExpressionWrapper, F,
                              FloatField, Sum, Value)
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from cashier.models import Invoice, Product, Sale, Member
from cashier.serializers.invoice import InvoiceSerializer
from cashier.serializers.sale import SaleSerializer
from cashier.services.common import common_services
from cashier.services.member import member_services
from cashier.services.products import product_services


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
        else:
            harga = product.selling_price
        return harga

    @action(detail=False, methods=['POST'])
    def add_item(self, request):
        """add_item."""
        invoice_number = request.POST.get('invoice_number')
        barcode = request.POST.get('barcode')
        qty = request.POST.get('qty')
        total = request.POST.get('total')
        member = request.POST.get('member')
        member = member_services.get_member_by_id(member)
        try:
            invoice = Invoice.objects.get(invoice=invoice_number)
            invoice.member = member
            invoice.save()
        except Exception as e:
            invoice = Invoice.objects.create(invoice=invoice_number, cashier=self.request.user, member=member)
        product = Product.objects.get(barcode=barcode)
        harga_bertingkats = product.hargabertingkat.all() 
        
        is_out_of_stock = product_services.check_product_stock(product, int(qty))
        if not is_out_of_stock:
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
                    'price': harga,
                    'is_out_of_stock': False}
        else:
            context = {'product': model_to_dict(product),
                'is_out_of_stock': True}

        return Response(context)

    @action(detail=False, methods=['POST'])
    def get_by_invoice(self, request):
        """get_by_invoice."""
        invoice_number = request.POST.get('invoice_number')
        try:
            invoice = Invoice.objects.filter(invoice=invoice_number)
            invoice_serializer = InvoiceSerializer(invoice, many=True)
            invoice_result = invoice_serializer.data
            
            queryset = self.get_queryset().filter(invoice=invoice.first())
            serializer = self.get_serializer(queryset, many=True)
            result = serializer.data
            context = {
                'sale_items':result,
                'invoice': invoice_result
                }
        except Exception as e:
            context = None
        return Response(context)

    @action(detail=False, methods=['POST'])
    def process_payment(self, request):
        """get_by_invoice."""
        invoice_number = request.POST.get('invoice_number')
        cash = request.POST.get('cash')
        change = request.POST.get('change')
        total = request.POST.get('total')
        member = request.POST.get('member')
        member = member_services.get_member_by_id(member)

        invoice = Invoice.objects.get(invoice=invoice_number)
        invoice.cash = cash
        invoice.change = change
        invoice.total = total
        invoice.status = 1
        invoice.cashier = self.request.user
        invoice.member = member
        invoice.save(update_fields=["cash", "cashier", "change", "total", "member", "status"])

        return HttpResponse(status=202)

    @action(detail=False, methods=['POST'])
    def delete_item(self, request):
        """delete_item."""
        invoice_number = request.POST.get('invoice_number')
        barcode = request.POST.get('barcode')

        invoice = Invoice.objects.get(invoice=invoice_number)
        product = Product.objects.get(barcode=barcode)

        item = Sale.objects.get(invoice=invoice, product=product)
        product.stock+=item.qty
        product.save(update_fields=["stock"])
        item.delete()
        return Response(model_to_dict(item))

    @action(detail=False, methods=['POST'])
    def update_item(self, request):
        """update_item."""
        is_out_of_stock = None
        invoice_number = request.POST.get('invoice_number')
        barcode = request.POST.get('barcode')
        new_qty = int(request.POST.get('qty'))
        # new_total = request.POST.get('total')

        invoice = Invoice.objects.get(invoice=invoice_number)
        product = Product.objects.get(barcode=barcode)
        item = Sale.objects.get(invoice=invoice, product=product)
        
        if item.qty < new_qty:
            qty_addition = new_qty - item.qty
            is_out_of_stock = product_services.check_product_stock(product, qty_addition)
        
        if not is_out_of_stock:
            if(item.qty<new_qty):
                product.stock-=(new_qty-item.qty)
            else:
                product.stock+=(item.qty-new_qty)
            product.save(update_fields=["stock"])
            
            harga = self.get_price(product, new_qty)
            item.qty = new_qty
            item.price = harga
            item.total = new_qty * harga
            item.save()
            context = {'sale': model_to_dict(item),
                        'is_out_of_stock': False}
        else:
            context = {'product': model_to_dict(product),
                'is_out_of_stock': True}

        return Response(context)

    @action(detail=False, methods=['POST'])
    def sale_report_by_product(self, request):
        date_range = request.POST.getlist('date_range[]')
        dates = common_services.convert_date_to_utc(date_range)

        product_sales_date_filter = Sale.objects.filter(invoice__status=1, invoice__date__range=dates)
        product_sales = product_sales_date_filter.values('product').annotate(Count("product")).values('product')

        products = product_sales_date_filter.filter(product__in=product_sales)\
            .values('product__barcode', 'product__selling_price', 'product__name',)\
            .annotate(qty_total=Sum("qty"))\
            .annotate(total_penjualan=ExpressionWrapper(F('qty_total')*F('product__selling_price'),   
                    output_field=FloatField()))

        return Response(products)

class ReportTransactionViewSet(viewsets.ModelViewSet):
    """ReportTransactionViewSet."""
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.order_by('created_at')

    @action(detail=False, methods=['POST'])
    def set_datatable(self, request):
        """set_datatable."""
        date_range = request.POST.getlist('date_range[]')
        dates = common_services.convert_date_to_utc(date_range)
        queryset = Invoice.objects.all()
        if date_range:
            queryset = queryset.filter(date__range=dates)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['POST'])
    def set_income_profit(self, request):
        """set_income."""
        condition = request.POST.get('date')
        if condition == '1':
            date_condition = datetime.now().date()
            data = Invoice.objects.filter(date__gte=date_condition)
            data_2 = Sale.objects.filter(created_at__gte=date_condition)
        elif condition == '2':
            date_condition = datetime.now().month
            data = Invoice.objects.filter(date__month=date_condition)
            data_2 = Sale.objects.filter(created_at__month=date_condition)
        elif condition == '3':
            date_condition = datetime.now().year
            data = Invoice.objects.filter(date__year=date_condition)
            data_2 = Sale.objects.filter(created_at__year=date_condition)
        elif condition == '4' :
            data = Invoice.objects.all()
            data_2 = Sale.objects.all()
        else :
            data = data_2 = ''
        
        income = 0
        for e in data:
            if  e.total == None :
                e.total = 0
            income += e.total
        
        profit = 0
        for a in data_2:
            product = Product.objects.get(name = a.product)
            profit += (product.selling_price - product.purchase_price)

        products = Product.objects.all()

        context={}
        context['income'] = income
        context['profit'] = profit
        context['date'] = datetime.now().date()
        # context['data'] = data
        context['data_2'] = data_2.values()
        context['product'] = products.values()
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
        # queryset = self.get_queryset()
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
        new_qty = int(request.POST.get('qty'))
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
        old_item_total = item.total
        item.price = SaleViewSet.get_price(self,product, new_qty)
        item.qty = new_qty
        item.total = new_qty * item.price
        item.save()

        invoice.total = (invoice.total - old_item_total) + item.total
        invoice.cash = cash
        invoice.change = change
        invoice.save()

        context = {
            'grand_total': invoice.total
        }

        return Response(context)
