from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile

#register
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

        error = next(iter(form.errors.get("__all__", [])), None)
        if error is None:
            # Prefer username/password field errors if present
            error = next(
                iter(form.errors.get("username", []) or form.errors.get("password", []) or []),
                "Please correct the errors below.",
            )
        return render(request, 'register.html', {"form": form, "error": error})

    return render(request, 'register.html', {"form": RegisterForm()})

#login
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("home")
        return render(request, "login.html", {"form": form})

    return render(request, "login.html", {"form": AuthenticationForm(request)})

#logout
@require_POST
def user_logout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('home')

#home
def home(request):
    return render(request, 'home.html')

#hire talent directory
def talent_list(request):
    profiles = UserProfile.objects.select_related('user').all()
    return render(request, 'talent_list.html', {'profiles': profiles})

#become an emploeyer
@login_required
def become_an_employer(request):
    if request.method == 'POST':
        employer_group, created = Group.objects.get_or_create(name='Employer')
        request.user.groups.add(employer_group)
        return redirect('employer_dashboard')
    
    # If GET request, show the confirmation form
    return render(request, 'become_an_employer.html')