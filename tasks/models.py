from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('ToDo', 'ToDo'),
        ('inProgress', 'inProgress'),
        ('Review', 'Review'),
        ('Done', 'Done')
    ]

    PRIORITY_CHOICES = [
        ('hoch', 'Hoch'),
        ('mittel', 'Mittel'),
        ('niedrig', 'Niedrig'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deadline = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='mittel')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ToDo')

    def __str__(self):
        return self.title

class Subtask(models.Model):
    task = models.ForeignKey(Task, related_name='subtasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.task.title} - {self.title}"
