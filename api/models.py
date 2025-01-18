from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
  # Optionale zusätzliche Felder für den Benutzer, z.B.:
  phone_number = models.CharField(max_length=20, blank=True)
  groups = models.ManyToManyField(Group, related_name='custom_user_groups')
  user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')

class Contact(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  # Optionale zusätzliche Felder für den Kontakt, z.B.:
  company = models.CharField(max_length=255, blank=True)

  def __str__(self):
    return self.user.username

class Task(models.Model):
  title = models.CharField(max_length=255)
  description = models.TextField(blank=True)
  due_date = models.DateField()
  category = models.CharField(max_length=255)  # Kann später durch ein Category-Modell ersetzt werden
  assigned_to = models.ManyToManyField(User, related_name='tasks')
  priority = models.CharField(max_length=20, choices=[
    ('low', 'Niedrig'),
    ('medium', 'Mittel'),
    ('high', 'Hoch'),
  ])
  status = models.CharField(max_length=20, choices=[
    ('planned', 'Geplant'),
    ('in_progress', 'In Bearbeitung'),
    ('review', 'Prüfen'),
    ('completed', 'Fertig'),
  ])

  def __str__(self):
    return self.title

class Subtask(models.Model):
  task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
  description = models.CharField(max_length=255)
  is_completed = models.BooleanField(default=False)

  def __str__(self):
    return self.description