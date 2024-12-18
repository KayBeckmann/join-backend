from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticated

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], url_path='change-status')
    def change_status(self, request, pk=None):
        task = self.get_object()
        new_status = request.data.get('status')
        # Validierung des Status
        if new_status not in dict(Task.STATUS_CHOICES):
            return Response({'error': 'Invalid status value'}, status=400)
        task.status = new_status
        task.save()
        return Response(TaskSerializer(task).data)