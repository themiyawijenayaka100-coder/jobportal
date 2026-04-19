from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Job
from django.shortcuts import get_object_or_404
from applications.models import Application

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

#employer dashboard
@login_required
def employer_dashboard(request):
    if not request.user.groups.filter(name='Employer').exists():
        return redirect('home')
    
    my_jobs = Job.objects.filter(created_by=request.user)
    
    return render(request, 'employer_dashboard.html', {'my_jobs': my_jobs})

@login_required
def manage_job_applications(request, job_id):
    job = get_object_or_404(Job, id=job_id, created_by=request.user)
    applications = Application.objects.filter(job=job)

    if request.method == 'POST':
        app_id = request.POST.get('application_id')
        new_status = request.POST.get('status')
        
        application = get_object_or_404(Application, id=app_id, job=job)
        application.status = new_status
        application.save()
        
        return redirect('manage_job_applications', job_id=job.id)

    return render(request, 'manage_applications.html', {'job': job, 'applications': applications})