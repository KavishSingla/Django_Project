from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import AppUser, Expense, Saving
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json




def home_view(request):
    return render(request, 'index.html')




def about_view(request):
    return render(request , 'about.html')



# # -----------------------CALCULATOR-----------------------------------------

def calculator_view(request):
    return render(request , 'cal_page.html')

def emi_view(request):
    return render(request , 'emiCalculator.html')

def fd_view(request):
    return render(request , 'fdCalculator.html')

def sip_view(request):
    return render(request , 'sipCalculator.html')

def rd_view(request):
    return render(request , 'rdCalculator.html')

def savings_view(request):
    return render(request , 'savingscalculator.html')


# # -----------------------CALCULATOR END-----------------------------------------

def expense_view(request):
    return render(request, 'expense.html')

def networth_view(request):
    return render(request , 'networth.html')

def check_it_out_view(request):
    return render(request , 'investing.html')

def contact_view(request):
    return render(request , 'contact.html')

def profile_view(request):
    return render(request , 'profile.html')






User = get_user_model()  # Use your custom user model
def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')


        if password != cpassword:
            messages.error(request, 'Passwords do not match')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
        else:
            try:
                validate_password(password)
                User.objects.create_user(
                    email=email,
                    name=name,
                    phone=phone,
                    
                    gender=gender,
                    password=password
                )
                messages.success(request, 'Registration successful! You can now login.')
                return redirect('login')
            except ValidationError as e:
                for error in e:
                    messages.error(request, error)
    return render(request, 'register.html')




def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        selected_role = request.POST.get('role')


        user = authenticate(request, email=email, password=password)
        if user:
            # Determine if the role matches the actual user status
            if (selected_role == 'admin' and user.is_superuser) or (selected_role == 'user' and not user.is_superuser):
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('home')
            else:
                messages.error(request, "Invalid credentials: Role mismatch")
        else:
            messages.error(request, 'Invalid email or password')
    return render(request, 'login.html',)


@csrf_exempt
@login_required
def add_expense(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        amount = float(data.get('amount'))
        saving = Saving.objects.get(user=request.user)

        if saving.amount < amount:
            return JsonResponse({'error': 'Insufficient savings'}, status=400)

        Expense.objects.create(user=request.user, title=title, amount=amount)
        saving.amount -= amount
        saving.save()

        return JsonResponse({'success': True, 'new_saving': saving.amount})

@csrf_exempt
@login_required
def update_savings(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        amount = float(data.get('amount'))

        saving, created = Saving.objects.get_or_create(user=request.user)
        saving.amount = amount
        saving.save()

        return JsonResponse({'success': True, 'new_saving': saving.amount})

@login_required
def get_data(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    saving = Saving.objects.get_or_create(user=request.user)[0]
    return JsonResponse({
        'savings': saving.amount,
        'expenses': [{'title': e.title, 'amount': e.amount} for e in expenses]
    })



@login_required
def update_user_view(request, user_id):
    user = AppUser.objects.get(id=user_id)


    if request.method == 'POST':
        user.name = request.POST.get('name')
        user.phone = request.POST.get('phone')
        user.gender = request.POST.get('gender')


        # Ensure unique product name per user
        # if AppUser.objects.filter(user=user, name=user.name).exclude(id=user_id).exists():
        #     messages.error(request, "Product with this name already exists.")
        # else:
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')


    return render(request, 'update_user.html', {'user': user})


@login_required
def delete_user_view(request, user_id):
    user = AppUser.objects.get(id=user_id)
    
    user.delete()
    messages.success(request, 'Product deleted successfully!')
   
    return redirect('profile')



@login_required
def all_profile_view(request):
    users = AppUser.objects.all()

    return render(request, 'all_profile.html' , context={'users':users})







@login_required
def view_profile(request):
    # if not request.user.is_superuser:
    #     messages.error(request, "Access denied: You are not authorized to view this page.")
    #     return redirect('dashboard')  # Redirect to dashboard or home instead of showing raw 403


    return render(request, 'profile.html')


@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('home')





