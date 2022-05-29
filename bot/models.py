from operator import mod
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User
from main.models import Articles


class Themes(models.Model):
    ids = models.IntegerField(
                verbose_name='IDS', 
                name='ids')
    theme = models.ForeignKey(
                to=Articles,
                on_delete=models.CASCADE, 
                name='theme',  
                verbose_name='Тема')

    def __str__(self):
        return f'{self.ids} - {self.theme}'

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'


class Questions(models.Model):
    # Вопросы и ответы бота
    question_text = models.CharField(
                verbose_name='Вопрос', 
                name='question_text', 
                max_length=255, 
                blank=True, 
                unique=True)
    chevy_words = models.TextField(
                verbose_name='Ключевые слова', 
                name='chevy_words',
                max_length=500,
                blank=True)

    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Keywords(models.Model):
    theme = models.BigIntegerField(
        verbose_name='Номер темы',  # Позже заменить связкой
        name='theme')
    keyword = models.CharField(
        verbose_name='Ключевое слово', 
        name='keyword',
        max_length=60,
        blank=True)

    def __str__(self):
        return self.keyword

    class Meta:
        verbose_name = 'Ключевое слово'
        verbose_name_plural = 'Ключевые слова'


class SettingsBot(models.Model):
    LEVEL_CHOICES = (
        ('short', "Низкий"),
        ('average', "Средний"),
        ('tall', "Высокий"),
    )
    user_id = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE, 
        name='user_id',  
        verbose_name='Пользователь', 
        unique=True)
    level = models.CharField(
        name='level', 
        verbose_name='Уровень настройки',
        max_length=10,
        choices=LEVEL_CHOICES)

    def __str__(self):
        return self.level

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'
