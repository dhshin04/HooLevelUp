from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    path('', views.today_schedule, name='today_schedule'),
    path('schedule-builder/',views.schedule_build, name='schedule_build'),
]
