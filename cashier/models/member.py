from django.db import models

from .base import BaseModel

class Member(BaseModel):
    """Member model."""
    name = models.CharField(max_length=128, db_index=True, verbose_name="nama")
    address = models.CharField(max_length=128, db_index=True, blank=True, null=True, verbose_name="alamat")
    phone = models.CharField(max_length=128, blank=True, null=True, verbose_name="no telp")
    

    def __str__(self):
        """String representation."""
        return self.name