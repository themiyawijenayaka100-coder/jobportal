from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import Application
from jobs.models import Job

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Security: Prevent applying to own job
    if job.created_by == request.user:
        return redirect('job_list')

    # Security: Prevent duplicate applications
    if Application.objects.filter(user=request.user, job=job).exists():
        return redirect('job_list')

    # Create the application
    Application.objects.create(
        user=request.user,
        job=job
    )

    return redirect('job_list')

def my_applications(request):
    apps = Application.objects.filter(user=request.user)
    return render(request, 'my_applications.html', {'apps': apps})