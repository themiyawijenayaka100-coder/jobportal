from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from .forms import RegisterForm, UserProfileForm, DirectMessageForm
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile, DirectMessage
from .models import Notification
from jobs.models import Job
from applications.models import Application
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash



# register
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

        error = next(iter(form.errors.get("__all__", [])), None)
        if error is None:
            error = next(
                iter(form.errors.get("username", []) or form.errors.get("password", []) or []),
                "Please correct the errors below.",
            )
        return render(request, 'register.html', {"form": form, "error": error})

    return render(request, 'register.html', {"form": RegisterForm()})


# login
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("home")
        return render(request, "login.html", {"form": form})

    return render(request, "login.html", {"form": AuthenticationForm(request)})


# logout
@require_POST
def user_logout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('home')


# home
def home(request):
    is_employer = (
        request.user.is_authenticated
        and request.user.groups.filter(name="Employer").exists()
    )

    context = {"is_employer": is_employer}

    if request.user.is_authenticated:
        profile, _ = UserProfile.objects.get_or_create(user=request.user)

        if is_employer:
            context.update(
                {
                    "active_jobs_count": Job.objects.filter(created_by=request.user).count(),
                    "total_applications_count": Application.objects.filter(
                        job__created_by=request.user
                    ).count(),
                }
            )
        else:
            recommended_jobs = list(
                Job.objects.exclude(created_by=request.user).order_by("-id")[:6]
            )
            status_by_job_id = dict(
                Application.objects.filter(user=request.user).values_list("job_id", "status")
            )
            for job in recommended_jobs:
                job.applied_status = status_by_job_id.get(job.id)

            context.update(
                {
                    "profile": profile,
                    "profile_incomplete": not (
                        (profile.bio or "").strip()
                        and (profile.skills or "").strip()
                        and (profile.experience or "").strip()
                        and (profile.education or "").strip()
                    ),
                    "recommended_jobs": recommended_jobs,
                    "recent_applications": Application.objects.select_related("job")
                    .filter(user=request.user)
                    .order_by("-applied_date")[:5],
                }
            )

    return render(request, "home.html", context)

#hire talent directory
@login_required
def talent_list(request):
    if not request.user.groups.filter(name="Employer").exists():
        return HttpResponseForbidden("Forbidden.")

    # Only show non-employer profiles to employers
    profiles = (
        UserProfile.objects.select_related("user")
        .exclude(user__groups__name="Employer")
        .order_by("user__username")
        .distinct()
    )
    return render(request, "talent_list.html", {"profiles": profiles})


# become an employer
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
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    profile_form = UserProfileForm(instance=profile, user=request.user)
    password_form = PasswordChangeForm(request.user)

    if request.method == "POST":
        if "save_profile" in request.POST:
            profile_form = UserProfileForm(
                request.POST,
                request.FILES,
                instance=profile,
                user=request.user
            )
            password_form = PasswordChangeForm(request.user)

            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect("edit_profile")

        elif "change_password" in request.POST:
            profile_form = UserProfileForm(instance=profile, user=request.user)
            password_form = PasswordChangeForm(request.user, request.POST)

            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password updated successfully.")
                return redirect("edit_profile")

    return render(request, "edit_profile.html", {
        "profile_form": profile_form,
        "password_form": password_form,
        "profile": profile,
    })


@login_required
def profile_detail(request, user_id: int):
    user_obj = get_object_or_404(User, pk=user_id)
    profile, _ = UserProfile.objects.get_or_create(user=user_obj)
    return render(
        request,
        "profile_detail.html",
        {"profile": profile, "profile_user": user_obj},
    )


def about_us(request):
    return render(request, "about.html")


@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by("-created_at")
    notifications.filter(is_read=False).update(is_read=True)
    return render(request, "notifications_list.html", {"notifications": notifications})


@login_required
def send_message(request, recipient_id: int):
    recipient = get_object_or_404(User, pk=recipient_id)

    if not request.user.groups.filter(name="Employer").exists():
        return HttpResponseForbidden("Only employers can initiate messages.")

    if recipient == request.user:
        return HttpResponseForbidden("You can't message yourself.")

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


@login_required
@require_POST
def mark_message_read(request, message_id: int):
    message_obj = get_object_or_404(DirectMessage, pk=message_id, recipient=request.user)
    if not message_obj.is_read:
        message_obj.is_read = True
        message_obj.save(update_fields=["is_read"])
    return JsonResponse({"ok": True, "message_id": message_obj.id})


@login_required
@require_POST
def delete_account(request):
    user_obj = request.user
    logout(request)
    user_obj.delete()
    messages.success(request, "Your account has been deleted.")
    return redirect("home")
