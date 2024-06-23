from django.db import models
from django.conf import settings
import datetime

# Create your models here.
class Task(models.Model):
  title = models.CharField(max_length=64)
  description = models.TextField(max_length=2048)
  state = models.PositiveSmallIntegerField(default=0)
  category = models.ForeignKey('Category', on_delete=models.CASCADE)
  assignedTo = models.ManyToManyField(settings.AUTH_USER_MODEL)
  dueDate = models.DateField(null=True, blank=True)
  priority = models.PositiveSmallIntegerField(default=0)
  created_at = models.DateField(default=datetime.date.today)
  subtasks = models.CharField(max_length=4098, null=True, blank=True)
  countSubtasks = models.PositiveSmallIntegerField(default=0)
  
  def __str__(self): #Overview in adminpanel
    return str(str(self.id) +": " + self.title + ", " + str(self.priority))

class Category(models.Model):
    name = models.CharField(max_length=32)
    color = models.CharField(max_length=32)

    def __str__(self): #Overview in adminpanel
        return self.name

class Subtask(models.Model):
    description = models.CharField(max_length=256)
    state = models.BooleanField(default=False)
    task = models.ForeignKey('Task', on_delete=models.CASCADE)

    def __str__(self): #Overview in adminpanel
        return self.description