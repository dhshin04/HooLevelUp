from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json

from llm_client import call_gemini
from . import prompts

# Create your views here.
def index(request):
    return HttpResponse('Hello')


def build(request):
    if request.method == 'POST':
        schedules = request.POST['items']
        return render(request, 'schedule/final_build.html', {'schedules': schedules})
    return render(request, 'schedule/build.html')


def generate(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        general_goal = data.get('general_goal', '')
        schedules = []

        if general_goal:
            prompt = prompts.schedule_prompt.format(general_goal=general_goal)
            llm_response = call_gemini(prompt)
            schedules = eval(llm_response)
        
        return JsonResponse({'schedules': schedules})
