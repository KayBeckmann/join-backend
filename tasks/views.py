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
    
    # path('task/', views.TaskList.as_view(), name='tasklist'),
    # path('task/<int:pk>/', views.TaskDetail.as_view(), name='taskdetail'),

class TaskList(generics.ListCreateAPIView):
  serializer_class = TaskOverviewSerializer

  def get_queryset(self):
    queryset = Task.objects.all()
    state = self.request.query_params.get('state')
    if state is not None:
      queryset = queryset.filter(taskState=state)
    return queryset

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = TaskAllSerializer
  queryset = Task.objects.all()

# class TaskList(APIView):
  # authentication_classes = [TokenAuthentication]
  # permission_classes = [IsAuthenticated]
  # 
  # def get(self, request, format=None):
    # tasks = Task.objects.all()
    # serializer = TaskAllSerializer(tasks, many=True)
    # return Response(serializer.data)

# class TaskOverview(APIView):
  # authentication_classes = [TokenAuthentication]
  # permission_classes = [IsAuthenticated]
# 
  # def get(self, request, format=None):
    # tasks = Task.objects.all()
    # serializer = TaskOverviewSerializer(tasks, many=True)
    # return Response(serializer.data)

# class CategoryView(APIView):
  # authentication_classes = [TokenAuthentication]
  # permission_classes = [IsAuthenticated]
  # 
  # def get(self, request, format=None):
    # categories = Category.objects.all()
    # serializer = CategorySerializer(categories, many=True)
    # return Response(serializer.data)
# 
# class SubtaskView(APIView):
  # authentication_classes = [TokenAuthentication]
  # permission_classes = [IsAuthenticated]
  # 
  # def get(self, request, format=None):
    # subtasks = Subtask.objects.all()
    # serializer = SubtaskSerializer(subtasks, many=True)
    # return Response(serializer.data)