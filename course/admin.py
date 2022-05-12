import imp
from django.contrib import admin
from .models import Articles, Categories, Tasks

admin.site.register(Categories)
admin.site.register(Articles)
admin.site.register(Tasks)
# Register your models here.
