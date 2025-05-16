import pytest
from django.urls import reverse, resolve
from expenses import views

def test_home_url():
    path = reverse("home")
    assert resolve(path).func == views.home

def test_add_expense_url():
    path = reverse("add_expense")
    assert resolve(path).func == views.add_expense

def test_add_supplier_url():
    path = reverse("add_supplier")
    assert resolve(path).func == views.add_supplier