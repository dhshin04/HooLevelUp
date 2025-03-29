from django.urls import path
from . import views

app_name = 'metric'

urlpatterns = [
    path('', views.index, name='index'),
]
