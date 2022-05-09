from django.urls import path
from .views import bot

urlpatterns = [
    path('', bot, name='bot'),
]
