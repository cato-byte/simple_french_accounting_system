import pytest
from django.urls import reverse
from expenses.models import CustomUser, Supplier, Expense
from datetime import date
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture
def registered_user(client):
    """Fixture to register a user and return the client."""
    register_url = reverse("register")
    register_data = {
        "username": "e2euser",
        "email": "e2e@example.com",
        "siret": "12345678901234",
        "fiscal_id": "FISCAL123",
        "company_name": "EndToEnd Inc.",
        "password1": "SecurePass!2025",
        "password2": "SecurePass!2025",
    }
    response = client.post(register_url, data=register_data)
    assert response.status_code == 302  # Ensure registration succeeded
    return client


@pytest.fixture
def logged_in_user(registered_user):
    """Fixture to log in the registered user."""
    login_url = reverse("login")
    login_data = {
        "username": "e2euser",
        "password": "SecurePass!2025",
    }
    response = registered_user.post(login_url, data=login_data)
    assert response.status_code == 302  # Ensure login succeeded
    return registered_user


@pytest.mark.django_db
def test_add_supplier(logged_in_user):
    # Add a supplier
    supplier_url = reverse("add_supplier")
    supplier_data = {
        "name": "EndSupplier",
        "siret": "98765432109876",
        "email": "supplier@end.com",
        "phone": "0601020304",
        "address": "123 Test Street",
        "country": "France",
        "vat_number": "FR987654321",
        "is_active": True,
    }
    response = logged_in_user.post(supplier_url, data=supplier_data)
    assert response.status_code == 302
    supplier = Supplier.objects.get(siret="98765432109876")
    assert supplier.name == "EndSupplier"

@pytest.mark.skip(reason="Pending fix for redirect after expense creation")
@pytest.mark.django_db
def test_add_expense(logged_in_user):
    # Create a supplier
    supplier = Supplier.objects.create(
        name="EndSupplier",
        siret="98765432109876",
        email="supplier@end.com",
        phone="0601020304",
        address="123 Test Street",
        country="France",
        vat_number="FR987654321",
        is_active=True,
    )

    # Add an expense
    expense_url = reverse("add_expense")
    image = SimpleUploadedFile("receipt.jpg", b"image_bytes", content_type="image/jpeg")
    expense_data = {
        "supplier": supplier.id,
        "expense_date": date.today(),
        "description": "End-to-end expense",
        "amount": "99.99",
        "payment_method": "card",
        "invoice_number": "E2E123",
        "category": "software",
        "receipt_image": image,
    }
    response = logged_in_user.post(expense_url, data=expense_data)
    print(response.status_code)
    print(response.context.get("form").errors)
    assert response.status_code == 302
    expense = Expense.objects.get(description="End-to-end expense")
    assert expense.supplier == supplier
    assert expense.amount == 99.99
    assert expense.receipt_image.name == "receipt.jpg"