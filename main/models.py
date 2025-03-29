from django.db import models
from django.contrib.auth.models import User
from skills.models import Skill

# ---------- Items ----------
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=50, choices=[('decor', 'Decoration'), ('level_up', 'Level Up')])

    def __str__(self):
        return self.name

# ---------- Inventory ----------
class Inventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_used = models.BooleanField(default=False)

# ---------- Quests ----------
class Quest(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    reward_coins = models.IntegerField(default=0)
    reward_xp = models.IntegerField(default=0)
    reward_item = models.ManyToManyField(Item, blank=True)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class UserQuest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    date_started = models.DateField()
    date_ended = models.DateField()
    is_completed = models.BooleanField(default=False)

# ---------- Coins / Currency ----------
class Coin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)

# ---------- Activity Logs ----------
class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    related_goal = models.ForeignKey(Skill, null=True, blank=True, on_delete=models.SET_NULL)

# ---------- Animals ----------
class Animal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)
