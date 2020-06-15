from django.db import models

from cashier.models import User

from .base import BaseModel

class Income(BaseModel):
    """Income model."""
    date = models.DateTimeField(auto_now_add=True)
    cashier = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    keterangan = models.CharField(max_length=128, db_index=True)
    jumlah_pemasukan = models.DecimalField(max_digits=9, decimal_places=0, null=True, blank=True)

    def __str__(self):
        """String representation."""
        return self.keterangan
