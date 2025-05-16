import pytest
from expenses.models import CustomUser, Supplier, Expense, ExpenseCategory
from datetime import date
from django.utils import timezone

@pytest.mark.django_db
def test_supplier_str():
    supplier = Supplier.objects.create(name="Test Supplier", siret="12345678901234")
    assert str(supplier) == "Test Supplier"

@pytest.mark.django_db
def test_expense_category_str():
    category = ExpenseCategory.objects.create(code="software", label="Logiciels")
    assert str(category) == "Logiciels"

@pytest.mark.django_db
def test_expense_str():
    user = CustomUser.objects.create_user(
        username="user1",
        email="user1@example.com",
        password="StrongPass123!",
        siret="12345678901234",
        company_name="TestCo"
    )
    supplier = Supplier.objects.create(name="Another Supplier", siret="98765432109876")
    expense = Expense.objects.create(
        user=user,
        supplier=supplier,
        expense_date=date.today(),
        description="A test expense",
        amount=50.00,
        payment_method="cash"
    )
    assert str(expense).startswith(str(date.today()))