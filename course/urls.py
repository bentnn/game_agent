from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('', views.index, name='course'),
    path('tasks', views.task, name='tasks'),
    path('tasks/taskpage', views.tasks, name='task'),
    path('/<str:name>', views.coursepage, name='task')
=======
    path('', views.home, name='course_home'),
    path('test/', views.test, name='test'),
>>>>>>> master
]
