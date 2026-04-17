from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# -------------------------
# REGISTER
# -------------------------
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Prevent duplicate usernames (IMPORTANT FIX)
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'Username already exists'
            })

        user = User.objects.create_user(username=username, password=password)
        login(request, user)

        return redirect('home')

    return render(request, 'register.html')


# -------------------------
# LOGIN
# -------------------------
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {
                'error': 'Invalid credentials'
            })

    return render(request, 'login.html')


# -------------------------
# LOGOUT
# -------------------------
def user_logout(request):
    logout(request)
    return redirect('home')


# -------------------------
# HOME
# -------------------------
def home(request):
    return render(request, 'home.html')