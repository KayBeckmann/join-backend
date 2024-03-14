from django.db import models
from django.conf import settings
import datetime

# Create your models here.
class TodoItem(models.Model):
  title = models.CharField(max_length=64)
  description = models.TextField(max_length=2048)
  category = models.ForeignKey('category', on_delete=models.CASCADE)
  assignedTo = models.ManyToManyField(settings.AUTH_USER_MODEL)
  dueDate = models.DateField(null=True, blank=True)
  priority = models.PositiveSmallIntegerField(default=1)
  created_at = models.DateField(default=datetime.date.today)
  
  
  def __str__(self): #Overview in adminpanel
    return str(str(self.id) +": " + self.title + ", " + str(self.priority))

class category(models.Model):
    name = models.CharField(max_length=32)
    color = models.CharField(max_length=32)

    def __str__(self): #Overview in adminpanel
        return self.name

class subtask(models.Model):
    description = models.CharField(max_length=256)
    state = models.BooleanField(default=False)
    task = models.ForeignKey('TodoItem', on_delete=models.CASCADE)

    def __str__(self): #Overview in adminpanel
        return self.description