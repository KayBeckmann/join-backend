from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.TaskView.as_view(), name='tasks'),
    path('categories/', views.CategoryView.as_view(), name='categories'),
    path('subtasks/', views.SubtaskView.as_view(), name='subtasks'),
]