from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Erweitertes User-Model mit zusätzlichen Feldern
    """
    is_admin = models.BooleanField(default=False, verbose_name="Administrator")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon")
    
    def __str__(self):
        return self.username
