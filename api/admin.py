from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Contact, Task, Subtask

User = get_user_model()

# Benutzerverwaltung anpassen (Custom User Admin)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'phone_number', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'phone_number')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'phone_number')}),
        ('Berechtigungen', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Wichtige Daten', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )

# Kontakt-Modell für Admin
class ContactAdmin(admin.ModelAdmin):
    list_display = ('user', 'company')
    search_fields = ('user__username', 'company')
    list_filter = ('company',)

# Task-Modell für Admin
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date', 'priority', 'status')
    list_filter = ('priority', 'status', 'due_date')
    search_fields = ('title', 'category', 'assigned_to__username')
    filter_horizontal = ('assigned_to',)

# Subtask-Modell für Admin
class SubtaskAdmin(admin.ModelAdmin):
    list_display = ('task', 'description', 'is_completed')
    list_filter = ('is_completed',)
    search_fields = ('task__title', 'description')

# Doppeltes User-Modell entfernen, falls bereits registriert
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

# Modelle in der Admin-Oberfläche registrieren
admin.site.register(User, CustomUserAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Subtask, SubtaskAdmin)
