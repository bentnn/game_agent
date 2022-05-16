from django.db import models
import uuid


class Categories(models.Model):
    title = models.CharField('Title', max_length=50)
    name = models.CharField('Name', max_length=50)
    priority = models.IntegerField('Priority')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    def __str__(self):
        return self.title


class Articles(models.Model):
    title = models.CharField('Title', max_length=50)
    name = models.CharField('Name', max_length=50)
    text = models.TextField('Text')
    category = models.ForeignKey(Categories, on_delete = models.SET_DEFAULT, default = 0)
    required = models.ManyToManyField('self', blank = True, symmetrical = False)

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'

    def __str__(self):
        return self.title

class Tasks(models.Model):
    LEVEL = (
        ('1', 'First'),
        ('2', 'Second'),
        ('3', 'Third'),
		('4', 'Fourth'),
		('5', 'Fifth')
    )
    taskId = models.UUIDField(db_index = True, default = uuid.uuid4, editable = False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    difficulty = models.CharField(max_length=1, choices=LEVEL)
    title = models.CharField('Title', max_length = 50)
    shortDescr = models.TextField('ShortDescr')
    fullDescr = models.TextField('FullDescr')
    neededThemes = models.ManyToManyField(Articles, blank = True, symmetrical = False)
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
    def __str__(self):
        return self.title
