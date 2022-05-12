from django.urls import path
from .views import bot, settings_bot, get_settings_bot

urlpatterns = [
    path('', bot, name='bot'),
    path('settings_bot', settings_bot, name='settings_bot'),
    path('get_settings_bot', get_settings_bot, name='get_settings_bot'),
]
