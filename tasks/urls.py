#path('tasks/', TaskView.as_view()),

from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.TaskView.as_view(), name='tasks'),
]