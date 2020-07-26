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

from cashier.models import Purchase, Product, PurchaseDetail, Supplier
from cashier.serializers.purchase import PurchaseSerializer
from cashier.serializers.purchase_detail import PurchaseDetailSerializer
from cashier.services.common import common_services
from cashier.services.supplier import supplier_services


class PurchaseDetailViewSet(viewsets.ModelViewSet):
    """ProductViewSet."""
    serializer_class = PurchaseDetailSerializer
    queryset = PurchaseDetail.objects.order_by('created_at')

    @action(detail=False, methods=['POST'])
    def add_item(self, request):
        """add_item."""
        invoice_purchase = request.POST.get('invoice_purchase')
        barcode = request.POST.get('barcode')
        qty = request.POST.get('qty')
        total = request.POST.get('total')
        supplier = request.POST.get('supplier')
        supplier = supplier_services.get_supplier_by_id(supplier)
        try:
            purchase = Purchase.objects.get(invoice=invoice_purchase)
        except Exception as e:
            purchase = Purchase.objects.create(invoice=invoice_purchase, cashier=self.request.user, supplier=supplier, total=0)

        product = Product.objects.get(barcode=barcode)

        try:
            purchase_item = PurchaseDetail.objects.get(invoice=purchase, product=product)
            new_qty = int(purchase_item.qty) + int(qty)
            harga = product.purchase_price
            new_total = new_qty * harga
            purchase_item.qty = new_qty
            purchase_item.total = new_total
            purchase_item.save(update_fields=['qty', 'total'])
        except Exception as e:
            print(e)
            harga = product.purchase_price
            total = int(qty) * harga
            purchase_item = PurchaseDetail.objects.create(invoice=purchase, product=product, qty=qty, total=total)

        purchase.total = purchase.total + purchase_item.total
        purchase.save(update_fields=['total'])
        
        context = {'purchase': model_to_dict(purchase_item),
                   'price': harga}

        return Response(context)

    @action(detail=False, methods=['POST'])
    def get_by_invoice(self, request):
        """get_by_invoice."""
        invoice_purchase = request.POST.get('invoice_purchase')
        try:
            purchase = Purchase.objects.filter(invoice=invoice_purchase)
            purchase_serializer = PurchaseSerializer(purchase, many=True)
            purchase_result = purchase_serializer.data
            
            queryset = self.get_queryset().filter(invoice=purchase.first())
            serializer = self.get_serializer(queryset, many=True)
            result = serializer.data
            context = {
                'purchase_items':result,
                'purchase': purchase_result
                }
        except Exception as e:
            context = None
        return Response(context)

    @action(detail=False, methods=['POST'])
    def process_payment(self, request):
        """get_by_invoice."""
        invoice_purchase = request.POST.get('invoice_purchase')
        total = request.POST.get('total')
        supplier = request.POST.get('supplier')
        supplier = supplier_services.get_supplier_by_id(supplier)
        payment_status = request.POST.get('payment_status')

        purchase = Purchase.objects.get(invoice=invoice_purchase)
        purchase.total = total
        purchase.cashier = self.request.user
        purchase.supplier = supplier
        purchase.status = 1
        purchase.payment_status = payment_status
        purchase.save(update_fields=["cashier", "total", "supplier", "status", "payment_status"])

        purchase_details = PurchaseDetail.objects.filter(invoice=purchase)
        for purchase_detail in purchase_details:
            product = Product.objects.get(name=purchase_detail.product)
            try:
                product.stock = product.stock + int(purchase_detail.qty)
                product.save(update_fields=["stock"])
            except Exception as e:
                print(e)

        return HttpResponse(status=202)

    @action(detail=False, methods=['POST'])
    def delete_item(self, request):
        """delete_item."""
        invoice_purchase = request.POST.get('invoice_purchase')
        barcode = request.POST.get('barcode')

        purchase = Purchase.objects.get(invoice=invoice_purchase)
        product = Product.objects.get(barcode=barcode)

        item = PurchaseDetail.objects.get(invoice=purchase, product=product)
        purchase.total -= item.total
        item.delete()
        purchase.save(update_fields=['total'])
        return Response(model_to_dict(item))

    @action(detail=False, methods=['POST'])
    def update_item(self, request):
        """update_item."""
        invoice_purchase = request.POST.get('invoice_purchase')
        barcode = request.POST.get('barcode')
        new_qty = int(request.POST.get('qty'))
        new_total = request.POST.get('total')

        purchase = Purchase.objects.get(invoice=invoice_purchase)
        product = Product.objects.get(barcode=barcode)

        item = PurchaseDetail.objects.get(invoice=purchase, product=product)

        item.qty = new_qty
        item.total = new_qty * product.purchase_price
        item.save()


        return Response(model_to_dict(item))

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

class ReportPurchaseViewSet(viewsets.ModelViewSet):
    """ReportPurchaseViewSet."""
    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.order_by('created_at')

    @action(detail=False, methods=['POST'])
    def set_datatable(self, request):
        """set_datatable."""
        date_range = request.POST.getlist('date_range[]')
        dates = common_services.convert_date_to_utc(date_range)

        if date_range:
            self.queryset = self.get_queryset().filter(date__range=dates)
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

"""
    @action(detail=False, methods=['POST'])
    def set_income_profit(self, request):
        """'''set_income.'''"""
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
"""    


class ReportPurchaseDetailViewSet(viewsets.ModelViewSet):
    """ReportPurchaseDetailViewSet."""
    serializer_class = PurchaseDetailSerializer
    queryset = PurchaseDetail.objects.order_by('created_at')

    @action(detail=False, methods=['POST'])
    def get_by_invoice(self, request):
        """get_by_invoice."""
        invoice_purchase = request.POST.get('invoice_purchase')
        queryset = self.get_queryset().filter(invoice=invoice_purchase)
        # queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def delete_item(self, request):
        """delete_item."""
        invoice_purchase = request.POST.get('invoice_purchase')
        barcode = request.POST.get('barcode')
        total = request.POST.get('total')
        qty = request.POST.get('qty')

        purchase = Purchase.objects.get(id=invoice_purchase)
        product = Product.objects.get(barcode=barcode)
        product.stock -= int(qty)
        product.save()

        item = PurchaseDetail.objects.get(invoice=purchase, product=product)
        item.delete()

        purchase.total = total
        purchase.save()

        return HttpResponse(status=201)

    @action(detail=False, methods=['POST'])
    def update_item(self, request):
        """update_item."""
        invoice_purchase = request.POST.get('invoice_purchase')
        barcode = request.POST.get('barcode')
        new_qty = int(request.POST.get('qty'))
        new_total = request.POST.get('total')
        grand_total = request.POST.get('grand_total')
        diff_qty = request.POST.get('diffQty')

        purchase = Purchase.objects.get(id=invoice_purchase)
        product = Product.objects.get(barcode=barcode)
        product.stock -= int(diff_qty)
        product.save()
        
        item = PurchaseDetail.objects.get(invoice=purchase, product=product)
        old_item_total = item.total
        item.qty = new_qty
        item.total = new_qty * item.price
        item.save()

        purchase.total = (purchase.total - old_item_total) + item.total
        purchase.save()

        context = {
            'grand_total': purchase.total
        }

        return Response(context)
