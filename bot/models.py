from operator import mod
from tabnanny import verbose
from django.db import models


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
