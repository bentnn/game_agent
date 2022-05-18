from django.contrib import admin
from requests import Session
from .models import Articles, Categories, Tasks, GoTests, JsTests, PythonTests, Sessions

admin.site.register(Categories)
admin.site.register(Articles)
admin.site.register(Tasks)
admin.site.register(GoTests)
admin.site.register(JsTests)
admin.site.register(PythonTests)
admin.site.register(Sessions)