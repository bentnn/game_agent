from rest_framework import serializers
from .models import Articles, Tasks


class ArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = ('title', 'text')


class NeededArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = ('title', 'name')


class TasksSerializer(serializers.ModelSerializer):
    neededThemes = NeededArticlesSerializer(read_only = True, many = True)
    class Meta:
        model = Tasks
        fields = ('title', 'neededThemes')

