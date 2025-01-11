from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import User, Task , Event
from .serializers import UserSerializer, TaskSerializer, EventSerializer
from .models import Statistic
from .serializers import StatisticSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Leaderboard
from .serializers import LeaderboardSerializer



# ViewSet для модели User
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Фильтрация пользователей на основе их роли (если нужно)
        role = self.request.query_params.get('role')
        if role:
            return self.queryset.filter(role=role)
        return self.queryset


# ViewSet для модели Task
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Координатор может создавать задачи
        if request.user.role != 'coordinator' or request.user.role != 'admin':
            return Response({'error': 'Only coordinators can create tasks.'}, status=403)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # Автоматически назначить координатора на задачу
        serializer.save(coordinator=self.request.user)

    def get_queryset(self):
        # Фильтрация задач на основе статуса (если нужно)
        status = self.request.query_params.get('status')
        if status:
            return self.queryset.filter(status=status)
        return self.queryset
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self,request,*args,**kwargs):

        if request.user.role != 'coordinator' or request.user.role != 'admin':
            return Response({'error':'Only coordinators can create Events'})
        return super().create(request,*args, **kwargs)
    def perform_create(self,serializer):
        serializer.save(coordinator = self.request.user)
     
    def get_queryset(self):
        # Filter events based on query parameters
        user = self.request.user
        if user.role == 'volunteer':
            # Volunteers see only the events they registered for
            return self.queryset.filter(registered_volunteers=user)
        elif user.role == 'coordinator':
            # Coordinators see the events they created
            return self.queryset.filter(coordinator=user)
        # Admins see all events
        return self.queryset

    def update(self, request, *args, **kwargs):
        # Only the coordinator of the event can update it
        event = self.get_object()
        if request.user != event.coordinator:
            return Response({'error': 'Only the coordinator of this event can update it.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Only the coordinator or an admin can delete an event
        event = self.get_object()
        if request.user != event.coordinator and request.user.role != 'admin':
            return Response({'error': 'Only the coordinator or an admin can delete this event.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)   


class LeaderboardViewSet(viewsets.ModelViewSet):
    queryset = Leaderboard.objects.all().order_by('-xp_points')  # Sorted by XP points
    serializer_class = LeaderboardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Everyone can see the leaderboard
        return self.queryset

    def create(self, request, *args, **kwargs):
        # Leaderboard entries are automatically created/updated through actions, no manual creation
        return Response({'error': 'Cannot manually create leaderboard entries.'}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        # Leaderboard is automatically updated, no manual updates
        return Response({'error': 'Cannot manually update leaderboard entries.'}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        # Deletion of leaderboard entries is not allowed
        return Response({'error': 'Cannot delete leaderboard entries.'}, status=status.HTTP_403_FORBIDDEN)

class StatisticViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Statistic.objects.all()
    serializer_class = StatisticSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # Return the latest statistics only
        queryset = self.get_queryset().order_by('-updated_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        # Allow fetching a specific statistic entry by ID
        return super().retrieve(request, *args, **kwargs)

