from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Articles, Categories, Tasks
from main.models import AboutUser
from .serializers import ArticlesSerializer, TasksSerializer, MenuArticlesSerializer
from course import course_manager, serializers
from .testing_manager import CodeExecutor
from django.http import JsonResponse


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
    
    def post(self, request, format = None):
        AboutUser.objects.get(user=request.user).passed_courses.add(Articles.objects.get(title=request.data.get("title")))
        return JsonResponse({'success': 'success'})

class TestingAPIView(APIView):
    def post(self, request, format = None):
        lang = request.data.get("lang")
        code = request.data.get("code")
        print("test")
        if (lang == "JavaScript"):
            test_res = CodeExecutor.jsCodeExecute(code)
            print({'output': test_res.stdout.decode("utf-8"), 'error': test_res.stderr.decode("utf-8")})
            return JsonResponse({'output': test_res.stdout.decode("utf-8"), 'error': test_res.stderr.decode("utf-8")})
        elif (lang == "Python"):
            test_res = CodeExecutor.pythonCodeExecute(code)
            print({'output': test_res.stdout.decode("ISO-8859-1"), 'error': test_res.stderr.decode("ISO-8859-1")})
            return JsonResponse({'output': test_res.stdout.decode("ISO-8859-1"), 'error': test_res.stderr.decode("ISO-8859-1")})
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