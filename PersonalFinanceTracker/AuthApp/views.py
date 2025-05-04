from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import AppUser
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as auth_login




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



def networth_view(request):
    return render(request , 'networth.html')

def check_it_out_view(request):
    return render(request , 'investing.html')

def contact_view(request):
    return render(request , 'contact.html')

# def profile_view(request):
#     return render(request , 'profile.html')
# @login_required
# def profile_view(request):
#     print(request.user.email())
#     return render(request, 'profile.html', {'user': request.user})





@login_required
def view_profile(request):
    return render(request, 'profile.html', {'user': request.user})






User = get_user_model()  # Use your custom user model


# def register_view(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
        
#         gender = request.POST.get('gender')
#         password = request.POST.get('password')
#         cpassword = request.POST.get('cpassword')


#         if password != cpassword:
#             messages.error(request, 'Passwords do not match')
#         elif User.objects.filter(email=email).exists():
#             messages.error(request, 'Email already registered')
#         else:
#             try:
#                 validate_password(password)
#                 User.objects.create_user(
#                     email=email,
#                     name=name,
#                     phone=phone,
                    
#                     gender=gender,
#                     password=password
#                 )
#                 messages.success(request, 'Registration successful! You can now login.')
#                 return redirect('login')
#             except ValidationError as e:
#                 for error in e:
#                     messages.error(request, error)
#     return render(request, 'register.html')

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
            return render(request, 'register.html')

        data = {
            'name': name,
            'email': email,
            'mobile': phone,
            'gender': gender,
            'password': password
        }

        try:
            response = requests.post('http://127.0.0.1:5000/registerapi', json=data)
            result = response.json()
            if response.status_code == 200:
                messages.success(request, result.get('message', 'Registration successful!'))
                return redirect('login')
            else:
                messages.error(request, result.get('error', 'Registration failed.'))
        except requests.exceptions.ConnectionError:
            messages.error(request, 'Failed to connect to Flask server.')

    return render(request, 'register.html')



# def login_view(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         selected_role = request.POST.get('role')


#         user = authenticate(request, email=email, password=password)
#         if user:
#             # Determine if the role matches the actual user status
#             if (selected_role == 'admin' and user.is_superuser) or (selected_role == 'user' and not user.is_superuser):
#                 login(request, user)
#                 messages.success(request, 'Login successful!')
#                 return redirect('home')
#             else:
#                 messages.error(request, "Invalid credentials: Role mismatch")
#         else:
#             messages.error(request, 'Invalid email or password')
#     return render(request, 'login.html',)


# ----------------------------------------------------------------------------------------------------

# def login_view(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         role = request.POST.get('role')

#         data = {
#             'email': email,
#             'password': password,
#             'role': role
#         }

#         try:
#             response = requests.post('http://127.0.0.1:5000/loginapi', json=data)
#             result = response.json()
#             if response.status_code == 200:
#                 token = result.get('access_token')
#                 request.session['jwt_token'] = token  # Store JWT if needed
#                 messages.success(request, result.get('message', 'Login successful!'))
#                 return redirect('home')
#             else:
#                 messages.error(request, result.get('error', 'Invalid credentials'))
#         except requests.exceptions.ConnectionError:
#             messages.error(request, 'Failed to connect to Flask server.')

#     return render(request, 'login.html')

# -----------------------------------------------------------------------------------------------------

from django.contrib.auth import login as auth_login

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        data = {
            'email': email,
            'password': password,
            'role': role
        }

        try:
            response = requests.post('http://127.0.0.1:5000/loginapi', json=data)
            result = response.json()
            if response.status_code == 200:
                token = result.get('access_token')
                request.session['jwt_token'] = token  # Store JWT token

                # Create or get user in Django's authentication system
                User = get_user_model()
                user, created = User.objects.get_or_create(email=email)

                # If this is a new user, set a random password (they'll authenticate via API)
                if created:
                    user.set_password(User.objects.make_random_password())
                    user.save()

                # Log the user into Django's authentication system
                auth_login(request, user)

                messages.success(request, result.get('message', 'Login successful!'))
                return redirect('home')
            else:
                messages.error(request, result.get('error', 'Invalid credentials'))
        except requests.exceptions.ConnectionError:
            messages.error(request, 'Failed to connect to Flask server.')

    return render(request, 'login.html')


# def login_view(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         role = request.POST.get('role')

#         data = {
#             'email': email,
#             'password': password,
#             'role': role
#         }

#         try:
#             response = requests.post('http://127.0.0.1:5000/loginapi', json=data)
#             result = response.json()
#             if response.status_code == 200:
#                 token = result.get('access_token')
#                 request.session['jwt_token'] = token  # Store JWT token
                
#                 # Create or get user in Django's authentication system
#                 User = get_user_model()
#                 user, created = User.objects.get_or_create(email=email)
                
#                 # If this is a new user, set a random password
#                 if created:
#                     import secrets
#                     import string
#                     alphabet = string.ascii_letters + string.digits
#                     random_password = ''.join(secrets.choice(alphabet) for i in range(12))
#                     user.set_password(random_password)
#                     user.save()
                
#                 # Manually log user into Django's auth system
#                 from django.contrib.auth import login as auth_login
#                 auth_login(request, user)
                
#                 messages.success(request, result.get('message', 'Login successful!'))
#                 return redirect('home')
#             else:
#                 messages.error(request, result.get('error', 'Invalid credentials'))
#         except requests.exceptions.ConnectionError:
#             messages.error(request, 'Failed to connect to Flask server.')

#     return render(request, 'login.html')

# ----------------------------------------------------------------------------------------------------

# @csrf_exempt
# def login_view(request):
#     print("Request method:", request.method)
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         print("email:", email)

#         # Call Flask API to check credentials
#         response = requests.post('http://127.0.0.1:5000/loginapi', json={
#             "email": email,
#             "password": password
#         })

#         if response.status_code == 200 and response.json().get("status") == "success":
#             # Create or get Django user, skip password check
#             jwt_token = response.json().get("access_token")
#             user, _ = User.objects.get_or_create(email=email)
#             login(request, user)  # Log in Django user directly
#             request.session['jwt_token'] = jwt_token

#             return redirect('home')  # or whatever protected view
#         else:
#             return JsonResponse({"error": "Invalid credentials"}, status=401)
#     else:
        

#         return JsonResponse({"error": "Invalid method"}, status=405)








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
def dashboard_view(request):
    return render(request, 'dashboard.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('home')





