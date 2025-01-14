from django.urls import path, include
from rest_framework.routers import DefaultRouter
from volonteer.views import (
    LoginView,
    UserViewSet,
    TaskViewSet,
    EventViewSet,
    LeaderboardViewSet,
    StatisticViewSet,
)
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")
router.register("tasks", TaskViewSet, basename="task")
router.register("events", EventViewSet, basename="event")
router.register("leaderboard", LeaderboardViewSet, basename="leaderboard")

urlpatterns = [
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/statistics/", StatisticViewSet.as_view({"get": "list"}), name="statistics"),
    path("api/", include(router.urls)),
]

