"""Product Model."""
from django.db import models

from cashier.models import Product, User, Supplier

from .base import BaseModel


class Purchase(BaseModel):
    """Purchase"""

    class PurchaseStatus(models.IntegerChoices):
        """PurchaseStatus choice."""
        ONPROCESS = 0
        SUCCESS = 1
        CANCEL = 2

    class PurchasePaymentStatus(models.IntegerChoices):
        """PurchaseStatus choice."""
        DEBT = 0
        CASH = 1

    invoice = models.CharField(max_length=128, db_index=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name="tanggal")
    cashier = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False, related_name='purchase_cashier', verbose_name="kasir")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=False, related_name='purchase_supplier')
    total = models.DecimalField(max_digits=9, decimal_places=0, null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=PurchaseStatus.choices, default=PurchaseStatus.ONPROCESS, db_index=True)
    payment_status = models.PositiveSmallIntegerField(choices=PurchasePaymentStatus.choices, default=PurchasePaymentStatus.CASH, db_index=True)

    def __str__(self):
        """String representation."""
        return self.invoice


class PurchaseDetail(BaseModel):
    """PurchaseDetail"""
    invoice = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='purchase_invoice')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchase_product', verbose_name="produk")
    purchase_price = models.DecimalField(max_digits=9, decimal_places=0, null=True, verbose_name="harga beli")
    qty = models.IntegerField(blank=False, null=False)
    total = models.DecimalField(max_digits=9, decimal_places=0)

    def __str__(self):
        """String representation."""
        return self.invoice.invoice + ' - ' + self.product.name
