from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Item)
admin.site.register(models.Inventory)
admin.site.register(models.Quest)
admin.site.register(models.UserQuest)
admin.site.register(models.Coin)
admin.site.register(models.ActivityLog)
admin.site.register(models.Animal)
