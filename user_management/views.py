from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

from user_management.models import User

# Create your views here.
# User = get_user_model()

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

@login_required
def update_password(request):
    """
    Allows a logged-in user to change their password.
    """
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        # Verify current password
        if not user.check_password(current_password):
            messages.error(request, "Your current password is incorrect.")
            return redirect('update-password')

        # Check that new passwords match
        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect('update-password')

        # Change password securely
        user.set_password(new_password)
        user.save()

        # Keep the user logged in after changing password
        update_session_auth_hash(request, user)

        messages.success(request, "Your password has been updated successfully.")
        return redirect('dashboard')  # redirect wherever appropriate

    return render(request, 'auth/update_password.html')

@login_required
def update_my_profile(request):
    """
    Allows the logged-in user to update their personal details.
    """
    user = request.user

    if request.method == "POST":
        # Get submitted data
        first_name = request.POST.get("first_name", "").strip()
        middle_name = request.POST.get("middle_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        gender = request.POST.get("gender", "")
        date_of_birth = request.POST.get("date_of_birth", "")
        country_code = request.POST.get("country_code", "")
        id_number = request.POST.get("id_number", "")
        id_type = request.POST.get("id_type", "")
        id_photo = request.FILES.get("id_photo")
        passport_photo = request.FILES.get("passport_photo")

        # Update user details
        user.first_name = first_name
        user.middle_name = middle_name
        user.last_name = last_name
        user.email = email
        user.gender = gender
        user.date_of_birth = date_of_birth or None
        user.country_code = country_code
        user.id_number = id_number
        user.id_type = id_type

        # Update phone only if it’s not conflicting with another user
        if phone and phone != user.phone:
            if User.objects.filter(phone=phone).exclude(id=user.id).exists():
                messages.error(request, "That phone number is already in use.")
                return redirect("update-profile")
            user.phone = phone

        # Handle photo uploads
        if id_photo:
            user.id_photo = id_photo
        if passport_photo:
            user.passport_photo = passport_photo

        user.save()
        messages.success(request, "Your profile has been updated successfully.")
        return redirect("profile")

    return render(request, "auth/update_profile.html", {"user": user})