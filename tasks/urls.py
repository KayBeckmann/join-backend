from django.urls import path
from . import views

urlpatterns = [
    path('task/', views.TaskList.as_view()),
    path('task/<int:pk>/', views.TaskDetail.as_view()),
    path('categorie/', views.CategoryList.as_view()),
    path('categorie/<int:pk>/', views.CategoryDetail.as_view()),
    path('subtasklist/', views.SubtaskList.as_view()),
    path('subtasklist/<int:pk>/', views.SubtaskDetail.as_view()),
]