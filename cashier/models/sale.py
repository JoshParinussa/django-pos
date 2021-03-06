"""Product Model."""
from django.db import models

from cashier.models import Product, User

from .base import BaseModel


class Invoice(BaseModel):
    """Invoice."""

    class InvoiceStatus(models.IntegerChoices):
        """StoreTier choice."""
        ONPROCESS = 0
        SUCCESS = 1
        CANCEL = 2

    invoice = models.CharField(max_length=128, db_index=True)
    date = models.DateTimeField(auto_now_add=True)
    cashier = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False, related_name='invoice_cashier', verbose_name="kasir")
    cash = models.DecimalField(max_digits=9, decimal_places=0, null=True, blank=True, verbose_name="tunai")
    change = models.DecimalField(max_digits=9, decimal_places=0, null=True, blank=True, verbose_name="kembalian")
    total = models.DecimalField(max_digits=9, decimal_places=0, null=True, blank=True)
    member = models.ForeignKey('Member', on_delete=models.CASCADE, null=True, blank=True, related_name='invoice_member')
    status = models.PositiveSmallIntegerField(choices=InvoiceStatus.choices, default=InvoiceStatus.ONPROCESS, db_index=True)

    def __str__(self):
        """String representation."""
        return self.invoice


class Sale(BaseModel):
    """Sales."""
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='invoice_sale')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_sale', verbose_name="produk")
    price = models.DecimalField(max_digits=9, decimal_places=0, null=True, verbose_name="harga")
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
