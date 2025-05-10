from django.shortcuts import render, redirect, get_object_or_404
from .models import UserAccount
from .forms import UserAccountForm

# Create your views here.
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'expenses/home.html')

def user_list(request):
    users = UserAccount.objects.all()
    return render(request, 'expenses/user_list.html', {'users': users})

def user_create(request):
    if request.method == 'POST':
        form = UserAccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserAccountForm()
    return render(request, 'expenses/user_form.html', {'form': form})

def user_deactivate(request, user_id):
    user = get_object_or_404(UserAccount, id=user_id)
    user.is_active = False
    user.save()
    return redirect('user_list')