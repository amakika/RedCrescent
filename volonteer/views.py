from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import User, Task, Event, Leaderboard, Statistic
from .serializers import UserSerializer, TaskSerializer, EventSerializer, LeaderboardSerializer, StatisticSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        role = self.request.query_params.get('role')
        if role:
            return self.queryset.filter(role=role)
        return self.queryset


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.role not in ['coordinator', 'admin']:
            return Response({'error': 'Only coordinators or admins can create tasks.'}, status=403)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(coordinator=self.request.user)

    def get_queryset(self):
        status_filter = self.request.query_params.get('status')
        if status_filter:
            return self.queryset.filter(status=status_filter)
        return self.queryset


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.role not in ['coordinator', 'admin']:
            return Response({'error': 'Only coordinators or admins can create events.'}, status=403)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(coordinator=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.role == 'volunteer':
            return self.queryset.filter(registered_volunteers=user)
        elif user.role == 'coordinator':
            return self.queryset.filter(coordinator=user)
        return self.queryset

    def update(self, request, *args, **kwargs):
        event = self.get_object()
        if request.user != event.coordinator and request.user.role != 'admin':
            return Response({'error': 'Only the coordinator or an admin can update this event.'}, status=403)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        event = self.get_object()
        if request.user != event.coordinator and request.user.role != 'admin':
            return Response({'error': 'Only the coordinator or an admin can delete this event.'}, status=403)
        return super().destroy(request, *args, **kwargs)


class LeaderboardViewSet(viewsets.ModelViewSet):
    queryset = Leaderboard.objects.all().order_by('-xp_points')
    serializer_class = LeaderboardSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        return Response({'error': 'Leaderboard entries are created automatically.'}, status=403)

    def update(self, request, *args, **kwargs):
        return Response({'error': 'Leaderboard entries are updated automatically.'}, status=403)

    def destroy(self, request, *args, **kwargs):
        return Response({'error': 'Leaderboard entries cannot be deleted.'}, status=403)


class StatisticViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Statistic.objects.all()
    serializer_class = StatisticSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by('-updated_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
