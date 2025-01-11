from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserViewSet,
    TaskViewSet,
    EventViewSet,
    LeaderboardViewSet,
    StatisticViewSet,
)

# Initialize the router
router = DefaultRouter()

# Register routes
router.register(r'users', UserViewSet, basename='user')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'events', EventViewSet, basename='event')
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')
router.register(r'statistics', StatisticViewSet, basename='statistic')

# Define urlpatterns
urlpatterns = [
    path('', include(router.urls)),  # Include all routes from the router
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
]
