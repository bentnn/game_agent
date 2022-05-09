from django.urls import path
from . import views
from course.views import ArticleAPIView

urlpatterns = [
    path('', views.index, name='course'),
    path('tasks', views.task, name='tasks'),
    path('tasks/taskpage', views.tasks, name='task'),
    path('<str:name>', views.coursepage, name='coursepage'),
    path('api/pages/', views.ArticleAPIView.as_view(), name='pages')
]
