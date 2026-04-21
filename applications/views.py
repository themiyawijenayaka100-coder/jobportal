from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Application
from jobs.models import Job

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Security: Prevent applying to own job
    if job.created_by == request.user:
        messages.error(request, "You can't apply to your own job post.")
        return redirect('job_list')

    application, created = Application.objects.get_or_create(user=request.user, job=job)
    if created:
        messages.success(request, "Application submitted.")
    else:
        messages.info(request, "You have already applied for this job.")

    return redirect('job_list')

def my_applications(request):
    apps = Application.objects.filter(user=request.user)
    return render(request, 'my_applications.html', {'apps': apps})