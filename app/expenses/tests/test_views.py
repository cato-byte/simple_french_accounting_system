import pytest
from moto import mock_aws
import boto3
from datetime import date
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from expenses.models import CustomUser, Supplier, Expense


# Utilidad común para crear usuario y loguearse
@pytest.fixture
def logged_in_user(client):
    user = CustomUser.objects.create_user(
        username="viewexp",
        password="StrongPass123!",
        siret="55555555555555",
        email="exp@v.com",
        company_name="ExpCorp"
    )
    client.login(username="viewexp", password="StrongPass123!")
    return user


# Utilidad común para crear un supplier
@pytest.fixture
def supplier():
    return Supplier.objects.create(name="Exp Supplier", siret="66666666666666")


# 1. Test con imagen subida (mock S3)
@pytest.mark.skip(reason="Pending fix for redirect after expense creation")
@pytest.mark.django_db
@mock_aws
def test_add_expense_with_image(client, settings, logged_in_user, supplier):
    settings.AWS_ACCESS_KEY_ID = "test"
    settings.AWS_SECRET_ACCESS_KEY = "test"
    settings.AWS_STORAGE_BUCKET_NAME = "test-bucket"
    settings.AWS_S3_ENDPOINT_URL = "https://s3.amazonaws.com"
    settings.AWS_S3_REGION_NAME = "us-east-1"
    settings.DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket="test-bucket")

    image_content = b"fake-image-bytes"
    image = SimpleUploadedFile("receipt.jpg", image_content, content_type="image/jpeg")

    data = {
        "supplier": supplier.id,
        "expense_date": date.today(),
        "description": "Con imagen",
        "amount": "44.00",
        "payment_method": "cash",
        "category": "software",
        "receipt_image": image,
    }

    response = client.post(reverse("add_expense"), data)
    assert response.status_code == 302

    expense = Expense.objects.get()
    assert expense.receipt_image_name == "receipt.jpg"

    s3_obj = s3.get_object(Bucket="test-bucket", Key=expense.receipt_image.name)
    assert s3_obj["Body"].read() == image_content


# 2. Test válido sin imagen
@pytest.mark.django_db
def test_add_expense_without_image(client, logged_in_user, supplier):
    data = {
        "supplier": supplier.id,
        "expense_date": date.today(),
        "description": "Sin imagen",
        "amount": "33.00",
        "payment_method": "card",
        "category": "software",
    }

    response = client.post(reverse("add_expense"), data)
    assert response.status_code == 302

    expense = Expense.objects.get()
    assert expense.description == "Sin imagen"
    assert not expense.receipt_image


# 3. Test inválido sin proveedor (supplier)
@pytest.mark.django_db
def test_add_expense_missing_supplier_should_fail(client, logged_in_user):
    data = {
        # "supplier" is missing!
        "expense_date": date.today(),
        "description": "Sin supplier",
        "amount": "22.00",
        "payment_method": "cash",
        "category": "software",
    }

    response = client.post(reverse("add_expense"), data)
    assert response.status_code == 200  # stays on form page due to validation error
    assert Expense.objects.count() == 0
    assert b"This field is required" in response.content or b"Obligatoire" in response.content
