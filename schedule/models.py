from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from skills.models import Skill

# Create your models here.
class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    

class Task(models.Model):
    schedule = models.ForeignKey(Schedule, related_name='tasks', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    estimated_time = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.description
