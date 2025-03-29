from django.db import models
from django.contrib.auth.models import User

# ---------- Skills ----------
class Skill(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    tier = models.IntegerField(default=1)
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='unlocks')

    def __str__(self):
        return self.name

class SkillProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)