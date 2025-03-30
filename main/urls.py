from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.main_screen, name='main_screen'),
    path('animal/<str:identifier>/', views.animal, name='animal'),
    path('settings/', views.settings_view, name='settings'),  # Renamed view to avoid Python keyword conflict
    path('profile/', views.profile, name='profile'),
    path('grant-rewards/<int:userquest_id>/', views.grant_rewards_for_quest, name='grant_rewards_for_quest'),
    path('add-test-data/', views.add_test_data, name='add_test_data'),
    path('complete-test-quest/', views.complete_test_quest, name='complete_test_quest'),
    path('apply-item/<str:animal_name>/', views.apply_item, name='apply_item'),


]

