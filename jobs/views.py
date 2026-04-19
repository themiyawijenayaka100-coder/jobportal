from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Job

# view all jobs
def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'job_list.html', {'jobs': jobs})

# create a job
@login_required
def create_job(request):
    # check if user is an employer
    if not request.user.groups.filter(name='Employer').exists():
        return HttpResponseForbidden("Access Denied: Only employers can post jobs. Please upgrade your account.")

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        company = request.POST['company']

        Job.objects.create(
            title=title,
            description=description,
            company=company,
            created_by=request.user
        )
        return redirect('job_list')

    return render(request, 'create_job.html')