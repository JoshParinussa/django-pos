"""Product Model."""
from django.db import models

from cashier.models import Product, User

from .base import BaseModel


class InvoiceStatus(models.IntegerChoices):
    """StoreTier choice."""
    EMPTY = 0
    SUCCESS = 1
    PENDING = 2


class Invoice(BaseModel):
    """Invoice."""
    invoice = models.CharField(max_length=128, db_index=True)
    date = models.DateTimeField(auto_now_add=True)
    cashier = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False, related_name='invoice_cashier')
    cash = models.DecimalField(max_digits=9, decimal_places=0, null=True, blank=True)
    change = models.DecimalField(max_digits=9, decimal_places=0, null=True, blank=True)
    total = models.DecimalField(max_digits=9, decimal_places=0, null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=InvoiceStatus.choices, default=InvoiceStatus.EMPTY, db_index=True)

    def __str__(self):
        """String representation."""
        return self.invoice


class Sale(BaseModel):
    """Sales."""
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='invoice_sale')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_sale')
    price = models.DecimalField(max_digits=9, decimal_places=0, null=True)
    qty = models.IntegerField(blank=False, null=False)
    total = models.DecimalField(max_digits=9, decimal_places=0)

    def __str__(self):
        """String representation."""
        return self.invoice.invoice + ' - ' + self.product.name


class Pembayaran(BaseModel):
    """Pembayaran."""
    tgl_pembayaran = models.DateTimeField(auto_now_add=True)
    pegawai = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    total = models.DecimalField(max_digits=9, decimal_places=0)
    products = models.ManyToManyField(Product, through='PembayaranProduct')


class PembayaranProduct(BaseModel):
    """PembayaranProduct."""
    pembayaran = models.ForeignKey('Pembayaran', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False, null=False)
    total = models.DecimalField(max_digits=9, decimal_places=0)
