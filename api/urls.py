# api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('csrf/', views.get_csrf_token, name='get_csrf_token'),  # Neue CSRF-Token-Route
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('user/', views.UserDetailView.as_view(), name='user-detail'),
    path('contact/', views.ContactDetailView.as_view(), name='contact-detail'),
    path('tasks/', views.TaskListView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/subtasks/', views.SubtaskListView.as_view(), name='subtask-list'),
    path('tasks/<int:pk>/subtasks/<int:subtask_pk>/', views.SubtaskDetailView.as_view(), name='subtask-detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
