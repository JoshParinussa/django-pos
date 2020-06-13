from django.db import models

from .base import BaseModel

class Member(BaseModel):
    """Member model."""
    name = models.CharField(max_length=128, db_index=True)
    address = models.CharField(max_length=128, db_index=True)
    phone = models.CharField(max_length=128, blank=False, null=False)
    profession = models.CharField(max_length=128, blank=False, null=False)
    

    def __str__(self):
        """String representation."""
        return self.name