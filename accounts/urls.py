from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('', views.home, name='home'),
    path("about/", views.about_us, name="about_us"),
    path('logout/', views.user_logout, name='logout'),
    path('become-employer/', views.become_an_employer, name='become_employer'),
    path('talents/', views.talent_list, name='talent_list'),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/<int:user_id>/", views.profile_detail, name="profile_detail"),
    path("notifications/", views.notifications_list, name="notifications_list"),
    path("messages/inbox/", views.inbox, name="inbox"),
    path("messages/send/<int:recipient_id>/", views.send_message, name="send_message"),
]