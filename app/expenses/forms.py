from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Button, HTML
from .models import CustomUser, Expense, Supplier
from django.utils.translation import gettext_lazy as _
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

class ExpenseForm(forms.ModelForm):
    receipt_image = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
                'receipt_image',  # 📷 move this to the top

                Row(
                    Column('supplier', css_class='col-md-10'),
                    Column(
                        HTML(
                            '<a href="{% url \'add_supplier\' %}?next={% url \'add_expense\' %}" '
                            'class="btn btn-outline-secondary mt-2">Add Supplier</a>'
                        ),
                        css_class='col-md-2'
                    )
                ),
                'expense_date',
                'description',
                'amount',
                'payment_method',
                'invoice_number',
                'category',

                Row(
                    Column(
                        Submit('submit', 'Add Expense', css_class='btn btn-primary me-2'),
                        Button('cancel', 'Cancel', css_class='btn btn-outline-secondary', onclick="window.history.back()"),
                        css_class='d-flex gap-2 align-items-center'
                    )
                )
            )

    class Meta:
        model = Expense
        fields = [
        'receipt_image',       
        'supplier',
        'expense_date',
        'description',
        'amount',
        'payment_method',
        'invoice_number',
        'category',
    ]
        widgets = {
            'expense_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 2}),
        }

    def clean_receipt_image(self):
        image = self.cleaned_data.get('receipt_image')
        if image and image.size > 5 * 1024 * 1024:  # 5 MB
            raise forms.ValidationError("Image file too large ( > 5MB ).")
        return image
    
    
class InvalidateExpenseForm(forms.Form):
    reason = forms.CharField(
        label=_("Reason for invalidation"),
        widget=forms.Textarea(attrs={"rows": 3}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'reason',
            Row(
                Submit('submit', 'Invalidate', css_class='btn btn-danger me-2'),
                Button('cancel', 'Cancel', css_class='btn btn-secondary', onclick="window.history.back()"),
                css_class='d-flex gap-2'
            )
        )


class SupplierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Add Supplier', css_class='btn btn-primary'))
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn btn-secondary', onclick="window.history.back()"))
    
    class Meta:
        model = Supplier
        fields = [
            'name',
            'siret',
            'email',
            'phone',
            'address',
            'country',
            'vat_number',
            'is_active',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Supplier Name'}),
            'siret': forms.TextInput(attrs={'placeholder': 'SIRET (14 digits)'}),
            'email': forms.EmailInput(attrs={'placeholder': 'example@email.com'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone number'}),
            'address': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Full address'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country'}),
            'vat_number': forms.TextInput(attrs={'placeholder': 'VAT number'}),
        }

    def clean_siret(self):
        siret = self.cleaned_data.get('siret')
        if siret and len(siret) != 14:
            raise forms.ValidationError("SIRET must be exactly 14 digits.")
        return siret
    
class UploadImageForm(forms.Form):
    receipt_image = forms.ImageField(required=True)