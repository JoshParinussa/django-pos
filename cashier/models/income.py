from django.db import models

from cashier.models import User

from .base import BaseModel

class Income(BaseModel):
    """Income model."""
    invoice = models.CharField(max_length=128, db_index=True, verbose_name="kode")
    date = models.DateTimeField(auto_now_add=True, verbose_name="tanggal")
    cashier = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False, verbose_name="kasir")
    keterangan = models.CharField(max_length=128, db_index=True)
    jumlah_pemasukan = models.DecimalField(max_digits=9, decimal_places=0, null=True, blank=True)

    def __str__(self):
        """String representation."""
        return self.keterangan
