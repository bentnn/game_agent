from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def test(request):
    return HttpResponse("<h1>Test course</h1>")
