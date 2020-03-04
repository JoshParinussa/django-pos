"""Product Model."""
from django.db import models

from cashier.models import Product, User

from .base import BaseModel


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
