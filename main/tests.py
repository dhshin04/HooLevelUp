from datetime import date
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Item, Inventory, Quest, UserQuest, Coin, Animal

def add_test_data(request):
    if not settings.DEBUG:
        return HttpResponse("Not allowed", status=403)

    if not request.user.is_authenticated:
        return HttpResponse("You must be logged in to add test data.", status=403)

    user = request.user

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

    return HttpResponse("Test data added successfully! Log in as 'testuser' to verify.")


def complete_all_quest(request):
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
        uq.save(update_fields=["is_completed"])
        completed_names.append(uq.quest.name)

    message = "Quests marked as complete: " + ", ".join(completed_names)
    return HttpResponse(message)


def complete_specific_quest(user, quest_id):
    try:
        uq = UserQuest.objects.get(user=user, quest__id=quest_id, is_completed=False)
        uq.is_completed = True
        uq.save()
        return f"Quest '{uq.quest.name}' marked as complete."
    except UserQuest.DoesNotExist:
        return "Quest not found or already completed."