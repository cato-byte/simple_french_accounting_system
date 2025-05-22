from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm,ExpenseForm, SupplierForm, InvalidateExpenseForm, UploadImageForm
from .models import Expense, Supplier
from django.utils import timezone
from django.urls import reverse

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .ocr_parsing import extract_fields_from_receipt_image


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



@login_required
def upload_receipt_image(request):
    """
    A separate view that handles only the image upload, runs OCR + NLP,
    and returns the add_expense form prefilled.
    """
    next_url = request.POST.get('next', reverse('user_expenses'))

    if request.method == 'POST':
        upload_form = UploadImageForm(request.POST, request.FILES)

        if upload_form.is_valid():
            image = upload_form.cleaned_data['receipt_image']
            parsed_fields = extract_fields_from_receipt_image(image, lang="fr")  # Language auto-detect later

            # Build prefilled expense form
            form = ExpenseForm(initial=parsed_fields)
            form.fields['receipt_image'].initial = image  # Optional: display but won't persist across submit

            return render(request, 'expenses/add_expense.html', {
                'form': form,
                'next': next_url,
                'ocr_preview': True
            })

        # Not valid: show upload form with errors
        return render(request, 'expenses/add_expense.html', {
            'upload_form': upload_form,
            'next': next_url
        })

    # If not POST, redirect to main form view
    return redirect('add_expense')

@login_required
def add_expense(request):
    supplier_id = request.GET.get('supplier_id')
    next_url = request.GET.get('next', reverse('user_expenses'))  # fallback if next not provided
    initial_data = {}
    if supplier_id:
        initial_data['supplier'] = get_object_or_404(Supplier, id=supplier_id)

    if request.method == 'POST':
        next_url = request.POST.get('next') or request.GET.get('next', reverse('user_expenses'))
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user

            # Handle receipt image upload
            image = form.cleaned_data.get('receipt_image')
            if image:
                username = request.user.username
                month_folder = timezone.now().strftime('%Y-%m')
                timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
                clean_name = image.name.replace(' ', '_')
                new_filename = f"{timestamp}_{username}_{clean_name}"
                s3_path = f"{username}/{month_folder}/{new_filename}"
                expense.receipt_image.name = s3_path
                expense.receipt_image_name = clean_name
                expense.receipt_image_uploaded_at = timezone.now()
                expense.receipt_image_path = s3_path

            expense.save()
            return redirect(next_url)
    else:
        form = ExpenseForm(initial=initial_data)

    return render(request, 'expenses/add_expense.html', {'form': form, 'next': next_url})



@login_required
def invalidate_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)

    if not expense.is_active:
        messages.warning(request, "This expense has already been invalidated.")
        return redirect('user_expenses')

    if request.method == "POST":
        form = InvalidateExpenseForm(request.POST)
        if form.is_valid():
            expense.is_active = False
            expense.invalidated_by = request.user
            expense.invalidated_at = timezone.now()
            expense.cancellation_reason = form.cleaned_data['reason']
            expense.save()

            messages.success(request, "Expense invalidated successfully.")
            return redirect('user_expenses')
    else:
        form = InvalidateExpenseForm()

    return render(request, 'expenses/invalidate_expense.html', {'form': form, 'expense': expense})

@login_required
def add_supplier(request):
    next_url = request.GET.get('next', '/dashboard/')  # Default fallback if not present

    if request.method == 'POST':
        next_url = request.POST.get('next') or request.GET.get('next', '/dashboard/')
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save()
            return redirect(f"{next_url}?supplier_id={supplier.id}")
    else:
        form = SupplierForm()

    return render(request, 'expenses/add_supplier.html', {'form': form, 'next': next_url})

@login_required
def user_expenses(request):
    show_all = request.GET.get('show_all') == '1'

    if show_all:
        expense_list = Expense.objects.filter(user=request.user).order_by('-expense_date')
    else:
        expense_list = Expense.objects.filter(user=request.user, is_active=True).order_by('-expense_date')

    paginator = Paginator(expense_list, 50)
    page_number = request.GET.get('page', 1)
    expenses = paginator.get_page(page_number)

    return render(request, 'expenses/user_expenses.html', {
        'expenses': expenses
    })

@login_required
def view_receipt(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    return render(request, 'expenses/view_receipt.html', {'expense': expense})