from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import User, Task, Event, Leaderboard, Statistic

# Custom AdminSite class to disable CSRF for admin views
class MyAdminSite(admin.AdminSite):
    @method_decorator(csrf_exempt)
    def admin_view(self, view, cacheable=False):
        return super().admin_view(view, cacheable)


# Create an instance of your custom admin site
admin_site = MyAdminSite(name="myadmin")

# Register models with the custom admin site
admin_site.register(User)
admin_site.register(Event)
admin_site.register(Leaderboard)
admin_site.register(Statistic)


# Customizing the TaskAdmin with CSRF exemption
@admin.register(Task, site=admin_site)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'photo')
