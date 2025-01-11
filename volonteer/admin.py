from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, Task, Event, Leaderboard, Statistic

admin.site.register(User)
admin.site.register(Task)
admin.site.register(Event)
admin.site.register(Leaderboard)
admin.site.register(Statistic)
