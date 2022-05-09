import imp
from django.contrib import admin
from .models import Articles, Categories

admin.site.register(Categories)
admin.site.register(Articles)
