import pytest
from expenses.forms import SupplierForm, ExpenseForm
from expenses.models import Supplier
from datetime import date

@pytest.mark.django_db
def test_supplier_form_valid():
    form_data = {
        "name": "Supplier Form",
        "siret": "12345678901234",
        "email": "email@supplier.com",
        "phone": "0600000000",
        "address": "1 Rue Exemple",
        "country": "France",
        "vat_number": "FR123456",
        "is_active": True,
    }
    form = SupplierForm(data=form_data)
    assert form.is_valid()

@pytest.mark.django_db
def test_supplier_form_invalid_siret():
    form = SupplierForm(data={"siret": "123"})
    assert not form.is_valid()
    assert "siret" in form.errors

@pytest.mark.django_db
def test_expense_form_valid():
    supplier = Supplier.objects.create(name="Form Supplier", siret="12345678901235")
    form_data = {
        "supplier": supplier.id,
        "expense_date": date.today(),
        "description": "Lunch",
        "amount": "25.50",
        "payment_method": "card",
        "invoice_number": "INV123",
        "category": "meals"
    }
    form = ExpenseForm(data=form_data)
    assert form.is_valid()