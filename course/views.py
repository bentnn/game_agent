from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Articles, Categories, Tasks
from main.models import AboutUser
from .serializers import ArticlesSerializer
from course import course_manager, serializers

class ArticleAPIView(APIView):
    serializer_class = ArticlesSerializer

    def get_queryset(self):
        articles = Articles.objects.all()
        return articles

    def get(self, request):
        try:
            title = request.query_params["title"]
            if (title is not None):
                article = Articles.objects.get(title = title)
                article_data = ArticlesSerializer(article)
        except:
            articles = self.get_queryset()
            article_data = ArticlesSerializer(articles, many = True)
        
        return Response(article_data.data)

@login_required(login_url='login')
def index(request):
    categories = Categories.objects.all().order_by('priority').values_list()
    values = {}
    user = request.user
    for category in categories:
        values.update({(category[1], category[2]): [(elem, course_manager.check_user(elem, request.user, request.user.is_superuser)) for elem in Articles.objects.filter(category = category[0])]})
    return render(request, 'course/content/index.html', {'categories': values})

@login_required(login_url='login')
def coursepage(request, name):
    return render(request, 'course/content/pages/' + name + '.html')

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
