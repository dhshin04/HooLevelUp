import math
from datetime import date
from django.conf import settings
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from .models import Item, Inventory, Quest, UserQuest, Coin, Animal
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .tests import add_test_data, complete_all_quest,complete_specific_quest

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


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                auth_login(request, user)
                messages.success(request, 'Registration successful.')
                return redirect('main:main_screen')
            except IntegrityError:
                form.add_error('username', 'This username is already taken.')
        else:
            messages.error(request, 'Registration failed. Please try again.')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('main:main_screen')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, '../templates/registration/login.html', {'form': form})

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


def add_test_data_view(request):
    return add_test_data(request)


def complete_all_quest_view(request):
    return complete_all_quest(request)


def complete_specific_quest_view(request, quest_id):
    if not settings.DEBUG:
        return HttpResponse("Not allowed", status=403)
    if not request.user.is_authenticated:
        return HttpResponse("You must be logged in to complete quests.", status=403)

    result_message = complete_specific_quest(request.user, quest_id)
    return HttpResponse(result_message)


@login_required
def add_quest(request):
    if not settings.DEBUG:
        return HttpResponse("Not allowed", status=403)

    user = request.user

    q1 = Quest.objects.create(
        name="1 task",
        description="Finish one task in schedule",
        reward_coins=50,
        reward_xp=20,
        hidden=False,
        is_daily=True
    )

    UserQuest.objects.create(
        user=user,
        quest=q1,
        date_started=date.today(),
        date_ended=date.today(),
        is_completed=False
    )

    return HttpResponse("Data added successfully!")