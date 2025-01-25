from django.urls import path
from . import views

urlpatterns = [
    path ('', views.home, name='home'),
    path('missions/list/', views.list_missions, name='list_missions'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('missions/', views.user_missions, name='user_missions'),
    path('missions/<int:mission_id>/', views.mission_detail, name='mission_detail'),
    path('missions/<int:mission_id>/complaint/', views.create_complaint, name='create_complaint'),
    path('missions/create/', views.create_mission, name='create_mission'),
    path('missions/<int:mission_id>/edit/', views.edit_mission, name='edit_mission'),
    path('missions/<int:mission_id>/delete/', views.delete_mission, name='delete_mission'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('consultants/create/', views.create_consultant, name='create_consultant'),
    path('consultants/assign_missions/', views.assign_missions, name='assign_missions'),
]