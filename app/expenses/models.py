from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    siret = models.CharField(max_length=14, unique=True)
    fiscal_id = models.CharField(max_length=50, blank=True, null=True)
    company_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    
class Supplier(models.Model):
    name = models.CharField(max_length=255)
    siret = models.CharField(max_length=14, unique=True)  # Required for legal traceability
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100, default="France")  # Might be foreign
    vat_number = models.CharField(max_length=20, blank=True, null=True)  # "numéro TVA intracommunautaire"
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class Expense(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('transfer', 'Bank Transfer'),
        ('cheque', 'Cheque'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    expense_date = models.DateField()
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    invoice_number = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)  # Optional tag
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.expense_date} - {self.amount}€ - {self.user.full_name}"