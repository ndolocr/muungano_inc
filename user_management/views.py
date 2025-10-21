from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
 

# Create your views here.
User = get_user_model()

def register_user(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Check if user already exists
        if User.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already registered.")
            return redirect('register')

        # Create user
        user = User.objects.create_user(
            phone=phone,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        messages.success(request, "Account created successfully. You can now log in.")
        return redirect('login')

    return render(request, 'auth/register.html')

def login_user(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        user = authenticate(request, phone=phone, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Welcome back!")
            return redirect('dashboard')  # Change to your home/dashboard page
        else:
            messages.error(request, "Invalid phone or password.")
            return redirect('login')

    return render(request, 'auth/login.html')

def logout_user(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')