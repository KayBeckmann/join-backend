from django.contrib import admin
from django.urls import path, include
from tasks.views import LoginView, TaskView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tasks.urls')),
]
