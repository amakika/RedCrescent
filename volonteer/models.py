from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework_simplejwt.tokens import RefreshToken


from cloudinary.models import CloudinaryField

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('volunteer', 'Volunteer'),
        ('coordinator', 'Coordinator'),
        ('admin', 'Admin'),
    ]
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    xp_points = models.IntegerField(default=0)
    profile_picture = CloudinaryField('image', null=True, blank=True)
    profile_picture_width = models.PositiveIntegerField(null=True, blank=True)
    profile_picture_height = models.PositiveIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.profile_picture:
            # Get image dimensions before saving
            image = self.profile_picture
            self.profile_picture_width = image.width
            self.profile_picture_height = image.height
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"






class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('expired', 'Expired'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    photo = CloudinaryField('image', null=True, blank=True)  # Use CloudinaryField for the photo
    assigned_volunteers = models.ManyToManyField(
        User, related_name='tasks', blank=True, limit_choices_to={'role': 'volunteer'}
    )
    coordinator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='coordinator_tasks', limit_choices_to={'role': 'coordinator'}
    )
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateTimeField()
    hours_to_complete = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.title

@receiver(post_save, sender=User)
def create_jwt_token(sender, instance, created, **kwargs):
    if created:
        # Создаем токены для нового пользователя
        refresh = RefreshToken.for_user(instance)
        # Можно сохранить или отправить токены пользователю
        print(f"Access Token: {refresh.access_token}")
        print(f"Refresh Token: {refresh}")




class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    coordinator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='coordinator_events', limit_choices_to={'role': 'coordinator'}
    )
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    registered_volunteers = models.ManyToManyField(User, related_name='registered_events', blank=True)
    is_public = models.BooleanField(default=False)  # New field for visibility

    def __str__(self):
        return self.title



class Leaderboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='leaderboard')
    rank = models.IntegerField(default=0)
    xp_points = models.IntegerField(default=0)
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.user.username} - Rank: {self.rank}"


class Statistic(models.Model):
    total_volunteers = models.IntegerField(default=0)
    total_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    male_volunteers = models.IntegerField(default=0)
    female_volunteers = models.IntegerField(default=0)
    other_gender_volunteers = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Global Statistics"

