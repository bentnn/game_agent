from rest_framework import serializers
import course
from .models import Articles, Categories, Tasks
from main.models import AboutUser
from course import course_manager


class ArticlesSerializer(serializers.ModelSerializer):
    is_passed = serializers.SerializerMethodField('get_is_passed')

    class Meta:
        model = Articles
        fields = ('is_passed', 'title', 'text')

    def get_is_passed(self, obj):
        return obj.users_set.filter(user=self.context['user']).exists()


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('title', 'name')


class MenuArticlesSerializer(serializers.ModelSerializer):
    is_available = serializers.SerializerMethodField('get_is_available')
    category = CategoriesSerializer(many=False)

    class Meta:
        model = Articles
        fields = ('is_available', 'title', 'name', 'category')

    def get_is_available(self, obj):
        return course_manager.check_user(obj, self.context['user'], self.context['is_superuser'])


class NeededArticlesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Articles
        fields = ('title', 'name')


class TasksSerializer(serializers.ModelSerializer):
    neededThemes = NeededArticlesSerializer(read_only=True, many=True)

    class Meta:
        model = Tasks
        fields = ('title', 'neededThemes')
