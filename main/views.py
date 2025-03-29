from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.
def main_screen(request):
    if not request.user.is_authenticated:
        return render(request, 'main.html')
    animals = Animal.objects.filter(user=request.user)
    quests = Quest.objects.filter(user=request.user)
    return render(request, 'main.html',{'animals':animals,'quests':quests})
def setup(request):
    return

def animal(request):
    return

def settings_view(request):
    return render(request, 'settings.html')

def profile(request):
    return render(request, 'profile.html')

"""
What to build 

main screen - 
"""