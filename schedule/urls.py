from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    path('', views.index, name='today_schedule'),
    path('build/',views.build, name='build'),
    path('generate/', views.generate, name='generate'),
    path('schedule_builder/', views.schedule_builder, name='schedule_builder'),
    path('complete/', views.complete_schedule, name='complete'),
]
