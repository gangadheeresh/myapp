from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile

# Home Page
def home(request):
    return render(request, 'home.html')

# Register
def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return render(request, 'register.html', {"error": "Passwords do not match"})

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {"error": "Username already taken"})

        user = User.objects.create_user(username=username, password=password)
        Profile.objects.create(user=user)  # create profile for image later
        return redirect('login')

    return render(request, 'register.html')

# Login
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'login.html', {"error": "Invalid credentials"})

    return render(request, 'login.html')

# Profile (with image upload)
@login_required
def profile_view(request):
    if request.method == "POST" and request.FILES.get('image'):
        profile = request.user.profile
        profile.image = request.FILES['image']
        profile.save()

    return render(request, 'profile.html', {"profile": request.user.profile})

# Logout
def logout_view(request):
    logout(request)
    return redirect('home')