from django.contrib import admin
from .models import Task, category, subtask

admin.site.register(Task)
admin.site.register(category)
admin.site.register(subtask)
