from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def metric(request):
    return HttpResponse('Hello Metric')
