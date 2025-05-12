from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button, Layout
from .models import CustomUser
import re

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Create Account', css_class='btn btn-primary'))
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn btn-secondary', onclick="window.history.back()"))


    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'siret', 'fiscal_id', 'password1', 'password2']

    def clean_password2(self):
        password = self.cleaned_data.get('password2')
        if len(password) < 12:
            raise forms.ValidationError("Password must be at least 12 characters long.")
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[^A-Za-z0-9]', password):
            raise forms.ValidationError("Password must contain at least one symbol.")
        return password
    
class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Login', css_class='btn btn-primary'))
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn btn-secondary', onclick="window.history.back()"))
