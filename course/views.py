from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Articles
from .serializers import ArticlesSerializer
from course import serializers

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
    return render(request, 'course/content/index.html')

@login_required(login_url='login')
def coursepage(request, name):
    return render(request, 'course/content/pages/' + name + '.html')

@login_required(login_url='login')
def tasks(request):
    return render(request, 'course/tasks/index.html')

@login_required(login_url='login')
def task(request):
    return render(request, 'course/tasks/taskpage.html')
