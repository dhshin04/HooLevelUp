from django.db import models
from django.contrib.auth.models import User
from skills.models import Skill

# Create your models here.
class Scheduler(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    skills = models.ManyToManyField(Skill, blank=True)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)