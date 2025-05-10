from django.db import models

class UserAccount(models.Model):
    full_name = models.CharField(max_length=255)
    siret = models.CharField(max_length=14, unique=True)
    fiscal_id = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name