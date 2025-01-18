from rest_framework import serializers
from .models import User, Contact, Task, Subtask

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username', 'email', 'first_name', 'last_name']  # Passe die Felder nach Bedarf an

class ContactSerializer(serializers.ModelSerializer):
  class Meta:
    model = Contact
    fields = '__all__'

class SubtaskSerializer(serializers.ModelSerializer):
  class Meta:
    model = Subtask
    fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
  subtasks = SubtaskSerializer(many=True, read_only=True)
  assigned_to = UserSerializer(many=True, read_only=True)

  class Meta:
    model = Task
    fields = '__all__'