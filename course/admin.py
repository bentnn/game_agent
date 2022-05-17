from django.contrib import admin
from .models import Articles, Categories, Tasks, GoTests, JsTests, PythonTests

admin.site.register(Categories)
admin.site.register(Articles)
admin.site.register(Tasks)
admin.site.register(GoTests)
admin.site.register(JsTests)
admin.site.register(PythonTests)
