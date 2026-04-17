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