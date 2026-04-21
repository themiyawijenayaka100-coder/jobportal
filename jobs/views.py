from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from .models import Job
from django.shortcuts import get_object_or_404
from applications.models import Application
from .forms import JobForm
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST

# view all jobs
def job_list(request):
    q = (request.GET.get("q") or "").strip()
    jobs_qs = Job.objects.all().order_by("-id")  # Show newest first

    if q:
        jobs_qs = jobs_qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
    
    if request.user.is_authenticated:
        # Get all applications for this user
        user_apps = Application.objects.filter(user=request.user)
        # Create a dictionary of {job_id: status}
        app_dict = {app.job_id: app.status for app in user_apps}

    paginator = Paginator(jobs_qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if request.user.is_authenticated:
        # Attach the status to each job on this page only
        for job in page_obj:
            job.applied_status = app_dict.get(job.id, None)

    return render(request, "job_list.html", {"page_obj": page_obj, "q": q})

# create a job
@login_required
def create_job(request):
    # check if user is an employer
    if not request.user.groups.filter(name='Employer').exists():
        return HttpResponseForbidden("Access Denied: Only employers can post jobs. Please upgrade your account.")

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.save()
            return redirect('job_list')
        return render(request, 'create_job.html', {"form": form})

    return render(request, 'create_job.html', {"form": JobForm()})


@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if job.created_by != request.user:
        messages.error(request, "Access denied: you can only edit your own job posts.")
        return redirect("job_list")

    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated successfully.")
            return redirect("employer_dashboard")
        return render(request, "edit_job.html", {"form": form, "job": job})

    form = JobForm(instance=job)
    return render(request, "edit_job.html", {"form": form, "job": job})


@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if job.created_by != request.user:
        messages.error(request, "Access denied: you can only delete your own job posts.")
        return redirect("job_list")

    if request.method == "POST":
        job.delete()
        messages.success(request, "Job deleted successfully.")
        return redirect("employer_dashboard")

    return render(request, "delete_job_confirm.html", {"job": job})

#employer dashboard
@login_required
def employer_dashboard(request):
    if not request.user.groups.filter(name='Employer').exists():
        return redirect('home')
    
    my_jobs = Job.objects.filter(created_by=request.user)
    total_active_jobs = my_jobs.count()
    total_pending_applications = Application.objects.filter(
        job__created_by=request.user, status="Pending"
    ).count()
    
    return render(
        request,
        "employer_dashboard.html",
        {
            "my_jobs": my_jobs,
            "total_active_jobs": total_active_jobs,
            "total_pending_applications": total_pending_applications,
        },
    )

@login_required
def manage_job_applications(request, job_id):
    job = get_object_or_404(Job, id=job_id, created_by=request.user)
    applications = Application.objects.filter(job=job)

    return render(request, 'manage_applications.html', {'job': job, 'applications': applications})


@login_required
@require_POST
def update_application_status(request):
    app_id = request.POST.get("application_id")
    new_status = request.POST.get("status")

    if not app_id or not new_status:
        return JsonResponse({"ok": False, "error": "Missing application_id or status."}, status=400)

    application = get_object_or_404(
        Application.objects.select_related("job"),
        id=app_id,
    )

    # Security: only the job owner can update statuses
    if application.job.created_by != request.user:
        return JsonResponse({"ok": False, "error": "Forbidden."}, status=403)

    valid_statuses = {choice[0] for choice in Application.STATUS_CHOICES}
    if new_status not in valid_statuses:
        return JsonResponse({"ok": False, "error": "Invalid status."}, status=400)

    application.status = new_status
    application.save(update_fields=["status"])

    return JsonResponse({"ok": True, "application_id": application.id, "status": application.status})