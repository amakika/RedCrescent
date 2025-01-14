from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from .models import User, Task, Event, Leaderboard, Statistic
from .serializers import (
    UserSerializer,
    TaskSerializer,
    EventSerializer,
    LeaderboardSerializer,
    StatisticSerializer,
)


class LoginView(APIView):
    """Login endpoint for JWT token generation."""
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": UserSerializer(user).data
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]



class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.role != 'coordinator' and request.user.role != 'admin':
            return Response({'error': 'Only coordinators can create tasks.'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(coordinator=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.role == "volunteer":
            return self.queryset.filter(assigned_volunteers=user)
        elif user.role == "coordinator":
            return self.queryset.filter(coordinator=user)
        return self.queryset

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def participate(self, request, pk=None):
        task = self.get_object()
        user = request.user

        if task.status != 'pending':
            return Response({'error': 'You can only join tasks that are pending.'}, status=status.HTTP_400_BAD_REQUEST)

        if task.current_volunteers >= task.volunteer_limit:
            return Response({'error': 'Task is already full.'}, status=status.HTTP_400_BAD_REQUEST)

        if user in task.assigned_volunteers.all():
            return Response({'error': 'You are already assigned to this task.'}, status=status.HTTP_400_BAD_REQUEST)

        task.assigned_volunteers.add(user)
        return Response({'success': f'You have successfully registered for the task "{task.title}".'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def leave(self, request, pk=None):
        task = self.get_object()
        user = request.user

        if user not in task.assigned_volunteers.all():
            return Response({'error': 'You are not assigned to this task.'}, status=status.HTTP_400_BAD_REQUEST)

        task.assigned_volunteers.remove(user)
        return Response({'success': f'You have successfully left the task "{task.title}".'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def change_status(self, request, pk=None):
        """Allow a coordinator or admin to change the status of a task."""
        task = self.get_object()

        if request.user.role not in ['coordinator', 'admin']:
            return Response({'error': 'Only coordinators or admins can change the task status.'}, status=status.HTTP_403_FORBIDDEN)

        new_status = request.data.get('status')
        if new_status not in dict(Task.STATUS_CHOICES).keys():
            return Response({'error': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)

        task.status = new_status
        task.save()
        return Response({'success': f'Task status updated to "{new_status}".'}, status=status.HTTP_200_OK)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.role not in ["coordinator", "admin"]:
            return Response({"error": "Only coordinators or admins can create events."}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(coordinator=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.role == "volunteer":
            return self.queryset.filter(registered_volunteers=user)
        elif user.role == "coordinator":
            return self.queryset.filter(coordinator=user)
        return self.queryset


class LeaderboardViewSet(viewsets.ModelViewSet):
    queryset = Leaderboard.objects.all().order_by("-xp_points")
    serializer_class = LeaderboardSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class StatisticViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        """Retrieve global statistics for coordinators."""
        if request.user.role != "coordinator":
            return Response({"error": "Only coordinators can access statistics."}, status=status.HTTP_403_FORBIDDEN)

        total_tasks = Task.objects.count()
        completed_tasks = Task.objects.filter(status="completed").count()
        total_events = Event.objects.count()
        volunteers = User.objects.filter(role="volunteer").count()
        coordinators = User.objects.filter(role="coordinator").count()

        return Response({
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "total_events": total_events,
            "volunteers_count": volunteers,
            "coordinators_count": coordinators
        })
