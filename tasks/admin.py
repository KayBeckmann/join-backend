from django.contrib import admin
from .models import TodoItem, category, subtask

admin.site.register(TodoItem)
admin.site.register(category)
admin.site.register(subtask)
