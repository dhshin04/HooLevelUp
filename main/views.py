import math
from datetime import date
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from .models import Item, Inventory, Quest, UserQuest, Coin, Animal

def get_user_coins(user):
    coin_obj = Coin.objects.filter(user=user).first()
    return coin_obj.coins if coin_obj else 0

def level_up_experience_calculate(level):
    return int(100 * math.pow(level, 1.5))

def main_screen(request):
    if not request.user.is_authenticated:
        return render(request, 'main.html')

    animals = Animal.objects.filter(user=request.user)
    user_quests = UserQuest.objects.filter(user=request.user)
    coins = get_user_coins(request.user)

    raw_xp = sum(animal.xp for animal in animals)
    level = 1
    remaining_xp = raw_xp
    while remaining_xp >= level_up_experience_calculate(level):
        remaining_xp -= level_up_experience_calculate(level)
        level += 1

    xp_needed = level_up_experience_calculate(level)
    xp_percentage = round((remaining_xp / xp_needed) * 100, 2) if xp_needed > 0 else 0

    context = {
        'animals': animals,
        'user_quests': user_quests,
        'coins': coins,
        'xp': xp_percentage,
        'raw_xp': raw_xp,
        'level': level,
        'user_xp': remaining_xp,
        'xp_needed': xp_needed,
        'xp_percentage': xp_percentage,
    }
    return render(request, 'main.html', context)


def animal(request, identifier):
    animal_obj = get_object_or_404(Animal, id=identifier, user=request.user)
    inventory_items = Inventory.objects.filter(user=request.user, item__type='level_up', quantity__gt=0)
    level = animal_obj.level
    next_level_xp = level_up_experience_calculate(level)
    xp_percentage = (animal_obj.xp / next_level_xp) * 100 if next_level_xp else 0
    return render(request, 'animal.html', {
        'animal': animal_obj,
        'inventory_items': inventory_items,
        'xp_percentage': xp_percentage,
        'xp_required': next_level_xp,
    })

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
    i1 = Item.objects.create(name="Golden Sword", description="A mighty sword that increases XP.", type="level_up", xp_reward=50)
    i2 = Item.objects.create(name="Flower Vase", description="A beautiful vase for decoration.", type="decor")
    Inventory.objects.create(user=user, item=i1, quantity=1)
    Inventory.objects.create(user=user, item=i2, quantity=2)
    q1 = Quest.objects.create(name="Collect 10 apples", description="Gather apples from the orchard.", reward_coins=50, reward_xp=20, hidden=False, is_daily=True)
    q2 = Quest.objects.create(name="Defeat the dragon", description="Slay the dragon terrorizing the village.", reward_coins=200, reward_xp=100, hidden=False, is_daily=False)
    UserQuest.objects.create(user=user, quest=q1, date_started=date.today(), date_ended=date.today(), is_completed=False)
    UserQuest.objects.create(user=user, quest=q2, date_started=date.today(), date_ended=date.today(), is_completed=False)
    Coin.objects.get_or_create(user=user, defaults={'coins': 100})
    Animal.objects.create(user=user, name="Lion", species="Panthera leo", level=1, xp=10)
    Animal.objects.create(user=user, name="Tiger", species="Panthera tigris", level=2, xp=50)
    return HttpResponse("Test data added successfully!")

def complete_test_quest(request):
    if not settings.DEBUG:
        return HttpResponse("Not allowed", status=403)
    if not request.user.is_authenticated:
        return HttpResponse("You must be logged in to complete quests.", status=403)
    user_quests = UserQuest.objects.filter(user=request.user, is_completed=False)
    if not user_quests.exists():
        return HttpResponse("No incomplete quests found for the current user.")
    completed_names = []
    for uq in user_quests:
        uq.is_completed = True
        uq.save()
        completed_names.append(uq.quest.name)
    return HttpResponse(f"Quests marked as complete: {', '.join(completed_names)}")

def grant_rewards_for_quest(request, userquest_id):
    if not settings.DEBUG:
        return HttpResponse("Not allowed", status=403)
    if not request.user.is_authenticated:
        return HttpResponse("You must be logged in to receive rewards.", status=403)
    user_quest = get_object_or_404(UserQuest, id=userquest_id, user=request.user, is_completed=True)
    quest = user_quest.quest
    coin_obj, created = Coin.objects.get_or_create(user=request.user, defaults={'coins': 0})
    coin_obj.coins += quest.reward_coins
    coin_obj.save()
    animals = Animal.objects.filter(user=request.user)
    total_xp_gain = quest.reward_xp
    xp_per_animal = total_xp_gain // animals.count() if animals else 0
    for animal in animals:
        animal.xp += xp_per_animal
        animal.save()
    new_total_xp = sum(a.xp for a in animals)
    level = 1
    remaining_xp = new_total_xp
    while remaining_xp >= level_up_experience_calculate(level):
        remaining_xp -= level_up_experience_calculate(level)
        level += 1
    reward_items_count = 0
    for item in quest.reward_item.all():
        inventory, created = Inventory.objects.get_or_create(user=request.user, item=item, defaults={'quantity': 0})
        inventory.quantity += 1
        inventory.save()
        reward_items_count += 1
    if quest.is_daily:
        user_quest.is_completed = False
        user_quest.date_started = date.today()
        user_quest.date_ended = date.today()
        user_quest.save()
        reset_flag = True
    else:
        user_quest.delete()
        reset_flag = False
    xp_percentage = (remaining_xp / level_up_experience_calculate(level)) * 100 if level_up_experience_calculate(level) else 0
    return JsonResponse({
        'message': f"Rewards granted for quest '{quest.name}': {quest.reward_coins} coins, {quest.reward_xp} XP, and {reward_items_count} reward items.",
        'coins': coin_obj.coins,
        'xp': xp_percentage,
        'level': level,
        'reset': reset_flag,
    })

def apply_item(request, animal_name):
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Not authenticated."}, status=403)

    animal = get_object_or_404(Animal, name=animal_name, user=request.user)
    inventory = Inventory.objects.filter(user=request.user, item__type='level_up', quantity__gt=0).first()

    if not inventory:
        return JsonResponse({"message": "No valid level-up item found."})

    xp_gain = inventory.item.xp_reward
    animal.xp += xp_gain
    animal.save()

    inventory.quantity -= 1
    inventory.save()

    total_needed = level_up_experience_calculate(animal.level)
    xp_percent = int((animal.xp / total_needed) * 100)

    return JsonResponse({
        "message": f"Applied {inventory.item.name}. {xp_gain} XP added to {animal.name}.",
        "new_xp": animal.xp,
        "new_quantity": inventory.quantity,
        "new_xp_percent": xp_percent
    })
