from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/', include('tasks.urls')),  # Neue URLs für Tasks & Kategorien
]
