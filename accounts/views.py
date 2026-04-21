from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import RegisterForm, UserProfileForm, DirectMessageForm
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile, DirectMessage

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


@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("edit_profile")
    else:
        form = UserProfileForm(instance=profile)

    return render(request, "edit_profile.html", {"form": form, "profile": profile})


@login_required
def send_message(request, recipient_id: int):
    recipient = get_object_or_404(User, pk=recipient_id)

    if request.method == "POST":
        form = DirectMessageForm(request.POST)
        if form.is_valid():
            message_obj = form.save(commit=False)
            message_obj.sender = request.user
            message_obj.recipient = recipient
            message_obj.save()
            messages.success(request, "Message sent.")
            return redirect("inbox")
    else:
        form = DirectMessageForm()

    return render(
        request,
        "send_message.html",
        {"form": form, "recipient": recipient},
    )


@login_required
def inbox(request):
    inbox_messages = DirectMessage.objects.select_related("sender", "recipient").filter(recipient=request.user)
    return render(request, "inbox.html", {"inbox_messages": inbox_messages})