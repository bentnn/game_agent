from django.shortcuts import render
from django.shortcuts import HttpResponse


def test(request):
    return HttpResponse("<h1>Test course</h1>")
