from rest_framework import serializers
from .models import Task, Category, Subtask

class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = ['id', 'title', 'done']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubtaskSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'category', 'user', 'deadline', 'priority', 'status', 'subtasks']
        read_only_fields = ['user']

    def create(self, validated_data):
        subtask_data = validated_data.pop('subtasks', [])
        task = Task.objects.create(**validated_data)
        for s_data in subtask_data:
            Subtask.objects.create(task=task, **s_data)
        return task

    def update(self, instance, validated_data):
        subtask_data = validated_data.pop('subtasks', None)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.deadline = validated_data.get('deadline', instance.deadline)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.save()

        # Subtasks aktualisieren, wenn welche übergeben wurden
        if subtask_data is not None:
            # Existierende Subtasks löschen und neu erstellen 
            # (Alternativ: smarteres Handling für Update)
            instance.subtasks.all().delete()
            for s_data in subtask_data:
                Subtask.objects.create(task=instance, **s_data)

        return instance
