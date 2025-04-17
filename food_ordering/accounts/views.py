from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from django.db import transaction
import traceback

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Basic validation
        if not all([username, email, password, confirm_password]):
            messages.error(request, "All fields are required")
            return redirect('register')
        
        if password != confirm_password:
            messages.error(request, "Passwords don't match")
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register')
        
        try:
            with transaction.atomic():
                # First create the user
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                
                # Check if profile already exists (shouldn't, but just in case)
                if not hasattr(user, 'profile'):
                    Profile.objects.create(user=user)
                
                messages.success(request, "Registration successful! Please login to continue.")
                return redirect('login')
                
        except Exception as e:
            error_message = f"Error during registration: {str(e)}\n{traceback.format_exc()}"
            print(error_message)  # This will print to the console for debugging
            if 'user' in locals():
                try:
                    user.delete()
                except:
                    pass
            messages.error(request, f"An error occurred during registration: {str(e)}")
            return redirect('register')
    
    return render(request, 'accounts/register.html')

def login_view(request):
    # Log out any existing user first
    logout(request)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def profile_view(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    
    if request.method == 'POST':
        profile.address = request.POST.get('address')
        profile.phone = request.POST.get('phone')
        profile.save()
        
        # Update user info
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')
        
    return render(request, 'accounts/profile.html', {'profile': profile})