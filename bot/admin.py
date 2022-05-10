from django.contrib import admin
from .models import Questions, Keywords


class AdminQuestion(admin.ModelAdmin):
    pass

admin.site.register(Questions)
admin.site.register(Keywords)
