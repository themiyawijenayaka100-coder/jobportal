from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from .models import Application
from jobs.models import Job
from accounts.models import Notification

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Security: Prevent applying to own job
    if job.employer == request.user:
        messages.error(request, "You can't apply to your own job post.")
        return redirect('job_list')

    application, created = Application.objects.get_or_create(user=request.user, job=job)
    if created:
        messages.success(request, "Application submitted.")
        applicant_name = request.user.get_full_name() or request.user.username
        Notification.objects.create(
            recipient=job.employer,
            message=f"{applicant_name} applied for {job.title}",
            link=f"/jobs/{job.id}/applications/",
        )
    else:
        messages.info(request, "You have already applied for this job.")

    return redirect('job_list')

@login_required
def my_applications(request):
    apps = Application.objects.select_related("job").filter(user=request.user).order_by("-applied_date")
    return render(request, "my_applications.html", {"apps": apps})


@login_required
@require_POST
def withdraw_application(request, application_id: int):
    application = get_object_or_404(
        Application.objects.select_related("job"),
        id=application_id,
    )

    # CRITICAL (IDOR protection): only the owner can withdraw
    if request.user != application.user:
        return HttpResponseForbidden("Forbidden.")

    if application.status != "Pending":
        messages.error(request, "Only pending applications can be withdrawn.")
        return redirect("my_applications")

    application.delete()
    messages.success(request, "Application withdrawn.")
    return redirect("my_applications")