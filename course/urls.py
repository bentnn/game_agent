from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='course'),
    path('tasks', views.task, name='tasks'),
    path('tasks/taskpage', views.tasks, name='task'),
    path('<str:name>', views.coursepage, name='coursepage')
]
