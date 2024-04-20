from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Task, Category, Subtask
from .serializers import UserSerializer, TaskAllSerializer, TaskOverviewSerializer, CategorySerializer, SubtaskSerializer

class LoginView(ObtainAuthToken):
  def post(self, request, *args, **kwargs):
    serializer = self.serializer_class(data=request.data, context={'request':request})
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    token, created = Token.objects.get_or_create(user=user)
    return Response({
      'token': token.key,
      'user_id': user.pk,
      'email': user.email
    })
    
class TaskList(generics.ListCreateAPIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  serializer_class = TaskOverviewSerializer

  def get_queryset(self):
    queryset = Task.objects.all()
    state = self.request.query_params.get('state')
    if state is not None:
      queryset = queryset.filter(taskState=state)
    return queryset

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]
  serializer_class = TaskAllSerializer
  queryset = Task.objects.all()

class CategoryList(generics.ListCreateAPIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]
  serializer_class = CategorySerializer
  queryset = Category.objects.all()

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]
  serializer_class = CategorySerializer
  queryset = Category.objects.all()

class SubtaskList(generics.ListCreateAPIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]
  serializer_class = SubtaskSerializer
  queryset = Subtask.objects.all()
  
  # def get_queryset(self):
    # queryset = Subtask.objects.all()
    # task = self.request.query_params.get('task')
    # if task is not None:
      # queryset = queryset.filter(subtaskTask=task)
      # return queryset

class SubtaskDetail(generics.RetrieveUpdateDestroyAPIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]
  serializer_class = SubtaskSerializer
  queryset = Subtask.objects.all()