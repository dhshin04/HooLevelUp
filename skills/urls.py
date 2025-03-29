from django.urls import path
from . import views

app_name = 'skills'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:skill_name>', views.skill_detail, name='skill_detail'),
]
