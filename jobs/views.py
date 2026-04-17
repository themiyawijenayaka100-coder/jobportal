from django.shortcuts import render, redirect
from .models import Job

def create_job(request):
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

        return redirect('create_job')

    return render(request, 'create_job.html')