from rest_framework import serializers
from .models import User, Task, Event, Leaderboard, Statistic


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    registered_volunteers = UserSerializer(many=True, read_only=True)
    coordinator = UserSerializer(read_only=True)

    class Meta:
        model = Event
        fields = '__all__'


class LeaderboardSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Leaderboard
        fields = '__all__'


class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        fields = '__all__'
