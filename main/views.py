from datetime import date
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Item, Inventory, Quest, UserQuest, Coin, Animal

def get_user_coins(user):
    coin_obj = Coin.objects.filter(user=user).first()
    return coin_obj.coins if coin_obj else 0

def main_screen(request):
    if not request.user.is_authenticated:
        return render(request, 'main.html')
    # Retrieve the logged-in user's data
    animals = Animal.objects.filter(user=request.user)
    user_quests = UserQuest.objects.filter(user=request.user)
    quests = [uq.quest for uq in user_quests]
    coins = get_user_coins(request.user)
    # Retrieve all items and the user's inventory (for test purposes)
    items = Item.objects.all()
    inventories = Inventory.objects.filter(user=request.user)
    # For XP, we sum up animal xp as a simple metric
    xp = sum(animal.xp for animal in animals)
    level = request.user.profile.level if hasattr(request.user, 'profile') else 1
    context = {
        'animals': animals,
        'quests': quests,
        'coins': coins,
        'xp': xp,
        'level': level,
        'items': items,
        'inventories': inventories,
    }
    return render(request, 'main.html', context)

def animal(request):
    return render(request, 'animal.html')

def settings_view(request):
    return render(request, 'settings.html')

def profile(request):
    return render(request, 'profile.html')

def add_test_data(request):
    if not settings.DEBUG:
        return HttpResponse("Not allowed", status=403)
    user, created = User.objects.get_or_create(username="testuser")

    Item.objects.all().delete()
    Inventory.objects.all().delete()
    Quest.objects.all().delete()
    UserQuest.objects.all().delete()
    Coin.objects.all().delete()
    Animal.objects.all().delete()

    # Create items and inventories
    i1 = Item.objects.create(name="Golden Sword", description="A mighty sword", type="level_up")
    i2 = Item.objects.create(name="Flower Vase", description="A beautiful vase", type="decor")
    Inventory.objects.create(user=user, item=i1, quantity=1)
    Inventory.objects.create(user=user, item=i2, quantity=2)
    # Create quests and a user quest
    q1 = Quest.objects.create(name="Collect 10 apples", description="Gather apples", reward_coins=50, reward_xp=20,
                              hidden=False, is_daily=True)
    q2 = Quest.objects.create(name="Defeat the dragon", description="Slay the dragon", reward_coins=200, reward_xp=100,
                              hidden=False, is_daily=False)
    UserQuest.objects.create(user=user, quest=q1, date_started=date.today(), date_ended=date.today(),
                             is_completed=False)
    # Create coin (avoid duplicate key error)
    Coin.objects.get_or_create(user=user, defaults={'coins': 100})
    # Create animals
    Animal.objects.create(user=user, name="Lion", species="Panthera leo", level=1, xp=10)
    Animal.objects.create(user=user, name="Tiger", species="Panthera tigris", level=2, xp=50)
    return HttpResponse("Test data added successfully!")


