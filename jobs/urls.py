from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_job, name='create_job'),
    path('dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('', views.job_list, name='job_list'),
]