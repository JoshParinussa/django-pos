from django.db import models

from .base import BaseModel

class Supplier(BaseModel):
    """Supplier model."""
    kode = models.CharField(max_length=32, db_index=True, blank=True, null=True)
    company_name = models.CharField(max_length=128, db_index=True, blank=True, null=True, verbose_name="nama perusahaan")
    address = models.CharField(max_length=128, db_index=True, blank=True, null=True, verbose_name="alamat")
    contact_person =  models.CharField(max_length=128, db_index=True, blank=True, null=True, verbose_name="nama kontak")
    office_phone = models.CharField(max_length=128, blank=True, null=True, verbose_name="no telp kantor")
    phone = models.CharField(max_length=128, blank=True, null=True, verbose_name="no HP")

    def __str__(self):
        """String representation."""
        return self.kode