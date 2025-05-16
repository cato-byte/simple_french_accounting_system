from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views
from .forms import CustomLoginForm

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('accounts/login/', auth_views.LoginView.as_view(
        authentication_form=CustomLoginForm
    ), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('expenses/add/', views.add_expense, name='add_expense'),
    path('suppliers/add/', views.add_supplier, name='add_supplier'),
    path('expenses/', views.user_expenses, name='user_expenses'),
    path('expenses/<int:pk>/invalidate/', views.invalidate_expense, name='invalidate_expense'),
    path('expenses/<int:pk>/receipt/', views.view_receipt, name='view_receipt'),
]