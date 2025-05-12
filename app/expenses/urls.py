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
]