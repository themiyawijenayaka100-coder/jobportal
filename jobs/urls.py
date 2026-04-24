from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_job, name='create_job'),
    path('<int:job_id>/edit/', views.edit_job, name='edit_job'),
    path('<int:job_id>/delete/', views.delete_job, name='delete_job'),
    path('dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('<int:job_id>/applications/', views.manage_job_applications, name='manage_job_applications'),
    path('applications/update-status/', views.update_application_status, name='update_application_status'),
    path("stories/", views.story_list, name="story_list"),
    path("stories/create/", views.create_story, name="create_story"),
    path('', views.job_list, name='job_list'),
]