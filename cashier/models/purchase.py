"""Product Model."""
from django.db import models

from cashier.models import Product, User, Supplier

from .base import BaseModel


class PurchaseStatus(models.IntegerChoices):
    """PurchaseStatus choice."""
    ONPROCESS = 0
    SUCCESS = 1


class Purchase(BaseModel):
    """Purchase"""
    invoice = models.CharField(max_length=128, db_index=True)
    date = models.DateTimeField(auto_now_add=True)
    cashier = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False, related_name='purchase_cashier')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=False, related_name='purchase_supplier')
    total = models.DecimalField(max_digits=9, decimal_places=0, null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=PurchaseStatus.choices, default=PurchaseStatus.ONPROCESS, db_index=True)

    def __str__(self):
        """String representation."""
        return self.invoice


class PurchaseDetail(BaseModel):
    """PurchaseDetail"""
    invoice = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='purchase_invoice')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchase_product')
    qty = models.IntegerField(blank=False, null=False)
    total = models.DecimalField(max_digits=9, decimal_places=0)

    def __str__(self):
        """String representation."""
        return self.invoice.invoice + ' - ' + self.product.name
