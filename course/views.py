import json
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from requests import Session
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Articles, Categories, Tasks, JsTests, GoTests, PythonTests, Sessions
from main.models import AboutUser
from .serializers import ArticlesSerializer, TasksSerializer, MenuArticlesSerializer
from course import course_manager, serializers
from .testing_manager import CodeExecutor
from django.http import JsonResponse
from django.contrib import messages
import json
from main.activity_func import norm_activity, add_activity, give_reward

class ArticleAPIView(APIView):
    serializer_class = ArticlesSerializer

    def get_queryset(self):
        articles = Articles.objects.all()
        return articles

    def get(self, request):
        try:
            title = request.query_params["title"]
            if title is not None:
                article = Articles.objects.get(title=title)
                article_data = ArticlesSerializer(article, context={'user': request.user})
        except Exception:
            articles = self.get_queryset()
            article_data = ArticlesSerializer(articles, many=True, context={'user': request.user})
        
        return Response(article_data.data)

class MenuArticleAPIView(APIView):
    serializer_class = MenuArticlesSerializer

    def get_queryset(self):
        articles = Articles.objects.all()
        return articles

    def get(self, request):
        articles = self.get_queryset()
        article_data = MenuArticlesSerializer(articles, many=True, context={'user': request.user, 'is_superuser': request.user.is_superuser})
        return Response(article_data.data)

    def post(self, request, format=None):
        if not request.user.is_superuser:
            about_user = AboutUser.objects.get(user=request.user)
            article = Articles.objects.get(title=request.data.get("title"))
            about_user.passed_courses.add(article)
            give_reward(about_user, article, request)
            # return JsonResponse({'success': 'success'})
        # AboutUser.objects.get(user=request.user).passed_courses.add(Articles.objects.get(title=request.data.get("title")))
        return JsonResponse({'success': 'success'})


class TestingAPIView(APIView):
    def post(self, request, format = None):
        lang = request.data.get("lang")
        code = request.data.get("code")
        taskId = request.data.get("task")
        if (lang == "JavaScript"):
            test = JsTests.objects.get(task=taskId)
            test_res = CodeExecutor.jsCodeExecute(code, test.test, taskId)
            if (not request.user.is_superuser):
                session = Sessions.objects.create(lang=lang, testResult=json.dumps(test_res), task_id=taskId, user=AboutUser.objects.get(user=request.user))
                session.save()
            return JsonResponse(test_res)
        elif (lang == "Python"):
            test = PythonTests.objects.get(task=taskId)
            test_res = CodeExecutor.pythonCodeExecute(code, test.test, taskId)
            if (not request.user.is_superuser):
                session = Sessions.objects.create(lang=lang, testResult=json.dumps(test_res), task_id=taskId, user=AboutUser.objects.get(user=request.user))
                session.save()
            return JsonResponse(test_res)
        elif (lang == "Go"):
            test = GoTests.objects.get(task=taskId)
            test_res = CodeExecutor.goCodeExecute(code, test.test, taskId)
            if (not request.user.is_superuser):
                session = Sessions.objects.create(lang=lang, testResult=json.dumps(test_res), task_id=taskId, user=AboutUser.objects.get(user=request.user))
                session.save()
            return JsonResponse(test_res)
        else:
            return JsonResponse({'output': 'None', 'error': 'None'})


class RequiredCoursesAPIView(APIView):
    serializer_class = TasksSerializer

    def get_queryset(self):
        tasks = Tasks.objects.all()
        return tasks

    def get(self, request, task_id = ''):
        try:
            if (task_id is not None):
                task = Tasks.objects.get(taskId = task_id)
                tasks_data = TasksSerializer(task)
        except:
            tasks = self.get_queryset()
            tasks_data = TasksSerializer(tasks, many = True)
        
        return Response(tasks_data.data)


@login_required(login_url='login')
def index(request, title = ''):
    print(title)
    categories = Categories.objects.all().order_by('priority').values()
    return render(request, 'course/content/index.html', {'categories': categories, 'coursename': title})


@login_required(login_url='login')
def tasks(request):
    tasks = list(Tasks.objects.all().order_by('created_at').values())
    for elem in tasks:
        elem['neededThemes'] = list(Tasks.objects.get(id = elem['id']).neededThemes.all().values('name'))
    themes = list(Articles.objects.all().order_by('title').values('title', 'name'))
    difficulty = Tasks.LEVEL
    return render(request, 'course/tasks/index.html', {'tasks': tasks, 'difficulties': difficulty, 'articles': themes})


@login_required(login_url='login')
def task(request, task_id = 0):
    task = Tasks.objects.get(id = task_id)
    return render(request, 'course/tasks/taskpage.html', {'task': task})
