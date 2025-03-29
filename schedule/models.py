from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Scheduler(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    goals = models.ManyToManyField(Goal, blank=True)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)