from django.db import models

class Articles(models.Model):
    title = models.CharField('Title', max_length=50)
    text = models.TextField('Text')
    
    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'
        
    def __str__(self):
        return self.title
