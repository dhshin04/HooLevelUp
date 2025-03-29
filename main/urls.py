from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.main_screen, name='main_screen'),
    path('setup/', views.setup, name='setup'),
    path('animal/<str:identifier>/', views.animal, name='animal'),
    path('settings/', views.settings_view, name='settings'),  # Renamed view to avoid Python keyword conflict
    path('profile/', views.profile, name='profile'),
]

