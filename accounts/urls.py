from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('', views.home, name='home'),
    path('logout/', views.user_logout, name='logout'),
    path('become-employer/', views.become_an_employer, name='become_employer'),
    path('talents/', views.talent_list, name='talent_list'),
]