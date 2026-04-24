from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('my/', views.my_applications, name='my_applications'),
    path("withdraw/<int:application_id>/", views.withdraw_application, name="withdraw_application"),
]