from django.contrib import admin
from .models import Questions, Keywords, SettingsBot, Themes


class AdminQuestion(admin.ModelAdmin):
    pass

admin.site.register(Questions)
admin.site.register(Keywords)
admin.site.register(SettingsBot)
admin.site.register(Themes)
