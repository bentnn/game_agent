from django.urls import path
from .views import bot, settings_bot, get_settings_bot, update_settings_bot, link_test_bot

urlpatterns = [
    path('', bot, name='bot'),
    path('settings_bot', settings_bot, name='settings_bot'),
    path('get_settings_bot', get_settings_bot, name='get_settings_bot'),
    path('update_settings_bot', update_settings_bot, name='update_settings_bot'),
    path('link_test_bot/<int:ids>', link_test_bot, name='link_test_bot'),
]
