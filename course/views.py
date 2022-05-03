from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
<<<<<<< HEAD
def index(request):
    return render(request, 'course/content/index.html')

@login_required(login_url='login')
def coursepage(request, str):
    return render(request, 'course/content/pages/' + str + '.html')

@login_required(login_url='login')
def tasks(request):
    return render(request, 'course/tasks/index.html')

@login_required(login_url='login')
def task(request):
    return render(request, 'course/tasks/taskpage.html')
=======
def test(request):
    return HttpResponse("<h1>Test course</h1>")


def home(request):
    return HttpResponse("<h1>Root of course app</h1>")
>>>>>>> master
