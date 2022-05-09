from django.db import models


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
    category = models.ForeignKey(Categories, on_delete=models.SET_DEFAULT, default=0)
    required = models.ManyToManyField('self', blank=True, symmetrical=False)

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'
        
    def __str__(self):
        return self.title
