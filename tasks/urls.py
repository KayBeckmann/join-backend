from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.TaskView.as_view(), name='tasks'),
    path('board/', views.TaskOverview.as_view(), name='board'),
    path('categories/', views.CategoryView.as_view(), name='categories'),
    path('subtasks/', views.SubtaskView.as_view(), name='subtasks'),
]