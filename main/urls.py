from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.main_screen, name='main_screen'),

    # Authentication
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='main:login'), name='logout'),

    # Menu
    path('settings/', views.settings_view, name='settings'),
    path('profile/', views.profile, name='profile'),

    path('animal/<str:identifier>/', views.animal, name='animal'),
    path('grant-rewards/<int:userquest_id>/', views.grant_rewards_for_quest, name='grant_rewards_for_quest'),
    path('apply-item/<str:animal_name>/', views.apply_item, name='apply_item'),

    # Test
    path('add-test-data/', views.add_test_data_view, name='add_test_data'),
    path('complete-all-quests/', views.complete_all_quest_view, name='complete_all_quests'),
    path('complete-quest/<int:quest_id>/', views.complete_specific_quest_view, name='complete_specific_quest'),
    path('add_quest/', views.add_quest, name='add_quest'),
]

