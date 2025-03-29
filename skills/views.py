from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def skills(request):
    return HttpResponse('Hello')


def skill_detail(request, skill_name):
    return HttpResponse(f'Some Skill: {skill_name}')
