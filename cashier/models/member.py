from django.db import models

from .base import BaseModel

class Member(BaseModel):
    """Member model."""
    name = models.CharField(max_length=128, db_index=True)
    address = models.CharField(max_length=128, db_index=True, blank=True, null=True)
    phone = models.CharField(max_length=128, blank=True, null=True)
    profession = models.CharField(max_length=128, blank=True, null=True)
    

    def __str__(self):
        """String representation."""
        return self.name