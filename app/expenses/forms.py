from django import forms
from .models import UserAccount

class UserAccountForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ['full_name', 'siret', 'fiscal_id', 'email', 'is_active']