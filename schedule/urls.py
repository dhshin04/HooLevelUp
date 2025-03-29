from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    path('', views.index, name='today_schedule'),
    path('build/',views.build, name='build'),
    path('generate/', views.generate, name='generate'),
]
