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
from .models import AppUser
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as auth_login
from django.shortcuts import get_object_or_404





def home_view(request):
    return render(request, 'index.html')




@login_required
def about_view(request):
    user = request.user

    flask_api_url = "http://127.0.0.1:5000/aboutus"
    jwt_token = request.session.get('jwt_token')  # Retrieve the token from the session

    headers = {
        'Authorization': f'Bearer {jwt_token}'  # Include the token in the Authorization header
    }

    try:
        response = requests.get(flask_api_url)
        if response.status_code == 200:
            about_info = response.json()
        else:
            about_info = {"error": "Could not fetch about us information"}
    except requests.exceptions.RequestException as e:
        about_info = {"error": f"Error occurred: {e}"}

    return render(request, 'about.html', {'user': user, 'about_info': about_info})



# # -----------------------CALCULATOR-----------------------------------------
@login_required
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





# @login_required
# def contact_view(request):


#     user = request.user

#     flask_api_url = "http://127.0.0.1:5000/contact"
#     jwt_token = request.session.get('jwt_token')  # Retrieve the token from the session

#     headers = {
#         'Authorization': f'Bearer {jwt_token}'  # Include the token in the Authorization header
#     }

#     try:
#         response = requests.get(flask_api_url)
#         if response.status_code == 200:
#             contact_info = response.json()  
#         else:
#             contact_info = {"error": "Could not fetch contact information"}
#     except requests.exceptions.RequestException as e:
#         contact_info = {"error": f"Error occurred: {e}"}

#     return render(request, 'contact.html', {'user': user, 'contact_info': contact_info})

@login_required
def contact_view(request):
    if request.method == 'POST':
        # print(request.POST)
        name_contact = request.POST.get('name_contact')
        email_contact = request.POST.get('email_contact')
        msg = request.POST.get('msg')
        data = {
            'name_contact': name_contact,
            'email_contact': email_contact,
            'msg': msg
            
        }
        try:
            response = requests.post('http://127.0.0.1:5000/contactapi', json=data)
            # print(f"Response Status Code: {response.status_code}")  # Debugging
            # print(f"Response Content: {response.text}")  # Debugging

            result = response.json()
            if response.status_code == 200:
                messages.success(request, result.get('message', 'message sent successfully'))
                return redirect('home')
            else:
                messages.error(request, result.get('error', ' failed.'))
        except requests.exceptions.ConnectionError:
            messages.error(request, 'Failed to connect to Flask server.')

    return render(request, 'contact.html')
    





@login_required
def all_contact_view(request):
    try:
        response = requests.get('http://127.0.0.1:5000/allcontactsapi')
        print(f"Response Status Code: {response.status_code}")  # Debugging
        print(f"Response Content: {response.text}")  # Debugging
        if response.status_code == 200:
            contact_data = response.json()
            print(contact_data)
        else:
            contact_data = []
            messages.error(request, "Failed to retrieve contacts.")
    except requests.exceptions.ConnectionError:
        contact_data = []
        messages.error(request, "Could not connect to the Flask server.")

    return render(request, 'all_contact.html', {'contacts': contact_data})







@login_required
def view_profile(request):
    
    return render(request, 'profile.html')






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
def all_contact_view(request):
    users = AppUser.objects.all()

    return render(request, 'all_contact.html' , context={'users':users})







@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('home')





