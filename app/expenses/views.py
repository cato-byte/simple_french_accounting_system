from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

# Create your views here.
from django.contrib.auth.decorators import login_required

import logging

logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'expenses/home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'User created successfully. You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'expenses/register.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'expenses/dashboard.html')