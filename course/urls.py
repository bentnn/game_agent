from django.urls import path
from . import views
from course.views import ArticleAPIView

urlpatterns = [
    path('', views.index, name='course'),
    path('tasks', views.tasks, name='tasks'),
    path('tasks/taskpage/<int:task_id>', views.task, name='taskpage'),
    path('<str:name>', views.coursepage, name='coursepage'),
    path('api/pages/', views.ArticleAPIView.as_view(), name='pages')
]
