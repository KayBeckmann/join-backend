from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login
from .models import User, Contact, Task, Subtask
from .serializers import UserSerializer, ContactSerializer, TaskSerializer, SubtaskSerializer
import datetime  # Import für Zeit- und Datumsfunktionen
import jwt  # Import für JWT-Token Erstellung
from django.conf import settings  # Zugriff auf Django Settings

# CSRF-Token bereitstellen
@api_view(['GET'])
def get_csrf_token(request):
    return Response({'csrfToken': get_token(request)})

# Registrierung
@api_view(['POST'])
def register(request):
    print("Empfangene Daten:", request.data)  # Debugging
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])  # Passwort korrekt hashen
        user.save()
        Contact.objects.create(user=user)  # Kontakt für den Benutzer erstellen
        login(request, user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# JWT-Token erstellen
def generate_jwt_token(user):
    payload = {
        'id': user.id,
        'username': user.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),  # Token gültig für 1 Tag
        'iat': datetime.datetime.utcnow(),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

@api_view(['POST'])
def login_view(request):
    print("Empfangene Daten:", request.data)  # Debugging
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username und Passwort erforderlich'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        token = generate_jwt_token(user)
        print(token)
        return Response({
            'message': 'Login erfolgreich',
            'username': user.username,
            'token': token
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Benutzer Detail und Update
class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# Kontakt Detail und Update
class ContactDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.contact

# Task List und Create
class TaskListView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Task.objects.all()
        return Task.objects.filter(assigned_to=user)

# Task Detail, Update und Delete
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Task.objects.all()
        return Task.objects.filter(assigned_to=user)

# Subtask List und Create
class SubtaskListView(generics.ListCreateAPIView):
    serializer_class = SubtaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        task_id = self.kwargs['pk']
        return Subtask.objects.filter(task_id=task_id)

    def perform_create(self, serializer):
        task_id = self.kwargs['pk']
        serializer.save(task_id=task_id)

# Subtask Detail, Update und Delete
class SubtaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubtaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        task_id = self.kwargs['pk']
        return Subtask.objects.filter(task_id=task_id)

# Dashboard API
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard(request):
    total_tasks = Task.objects.count()
    high_priority_tasks = Task.objects.filter(priority='high').count()
    next_due_date = Task.objects.order_by('due_date').values_list('due_date', flat=True).first()
    return Response({
        'total_tasks': total_tasks,
        'high_priority_tasks': high_priority_tasks,
        'next_due_date': next_due_date,
    })
