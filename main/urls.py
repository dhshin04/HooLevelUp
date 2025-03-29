from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.main_screen, name='main_screen'),
    path('accounts/',views.accounts,name='accounts'),
    path('setup/', views.setup, name='setup'),
    path('animals/<str:identifier>/', views.animals, name='animals'),
]
