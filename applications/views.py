from django.shortcuts import redirect
from .models import Application
from jobs.models import Job

def apply_job(request, job_id):
    job = Job.objects.get(id=job_id)

    Application.objects.create(
        user=request.user,
        job=job
    )

    return redirect('job_list')

from django.shortcuts import render
from .models import Application

def my_applications(request):
    apps = Application.objects.filter(user=request.user)
    return render(request, 'my_applications.html', {'apps': apps})