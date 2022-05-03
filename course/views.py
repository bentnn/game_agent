from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required


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
