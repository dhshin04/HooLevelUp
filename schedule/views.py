from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from django.contrib.auth.models import User
from django.utils import timezone
import json

from llm_client import call_gemini
from . import prompts
from . import models

def index(request):
    schedule = models.Schedule.objects.prefetch_related('tasks').first()
    return render(request, 'schedule/home.html', {'schedule': schedule})


def build(request):
    if request.method == 'POST':
        tasks = request.POST.get('items', '')
        tasks = eval(tasks)

        timestamps = []
        if tasks:
            prompt = prompts.timestamp_prompt.format(tasks=tasks)
            llm_response = call_gemini(prompt)
            timestamps = eval(llm_response)

        print(tasks, len(tasks))
        print(timestamps, len(timestamps))

        if len(tasks) != len(timestamps):
            return HttpResponseServerError('Internal Server Error: Tasks and Timestamps do not match in length')

        schedules = zip(tasks, timestamps)
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


def schedule_builder(request):
    data = request.POST.get('items')
    schedules = json.loads(data)

    dummy_user, _ = User.objects.get_or_create(username='demo')
    schedule, created = models.Schedule.objects.get_or_create(
        user=dummy_user,
        defaults={'name': 'My Schedule'},
    )

    # Update the name or timestamp if needed
    schedule.name = "My Schedule"
    schedule.created_at = timezone.now()
    schedule.save()

    # Clear existing tasks before adding new ones
    schedule.tasks.all().delete()

    for task, timestamp in schedules:
        models.Task.objects.create(
            schedule=schedule,
            description=task,
            estimated_time=timestamp,
        )

    return redirect('schedule:today_schedule')


def complete_schedule(request):
    if request.method == 'POST':
        schedule = models.Schedule.objects.prefetch_related('tasks').first()
        if not schedule:
            return redirect('schedule:today_schedule')

        checked_ids = request.POST.getlist('completed_tasks')
        all_ids = [task.id for task in schedule.tasks.all()]

        # ✅ Mark checked as complete
        models.Task.objects.filter(id__in=checked_ids).update(completed=True)

        # ❌ Mark unchecked as incomplete
        unchecked_ids = set(all_ids) - set(map(int, checked_ids))
        models.Task.objects.filter(id__in=unchecked_ids).update(completed=False)

        return redirect('schedule:today_schedule')
