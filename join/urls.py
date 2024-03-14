from django.contrib import admin
from django.urls import path
from tasks.views import LoginView, TaskView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('tasks/', TaskView.as_view()),
]
