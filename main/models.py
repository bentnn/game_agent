from django.db import models
from django.contrib.auth.models import User
from course.models import Articles

class Achievement(models.Model):
	name = models.CharField(max_length=70)
	icon = models.ImageField(upload_to="Achievements")

	class Meta:
		verbose_name = 'достижение'
		verbose_name_plural = 'достижения'

	def __str__(self):
		return self.name


class GameItems(models.Model):
	TYPES = (
		('fr', 'frame'),
		('bg', 'background'),
	)
	name = models.CharField(max_length=100)
	image = models.ImageField(upload_to='Items', blank=True)
	type = models.CharField(max_length=30, choices=TYPES, default='fr')
	price = models.SmallIntegerField(default=0)

	class Meta:
		# ordering = ('-date', )
		verbose_name = 'Игровой товар'
		verbose_name_plural = 'Игровые товары'

	def __str__(self):
		return self.name


class AboutUser(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	level = models.SmallIntegerField(default=0)
	exp_to_level = models.SmallIntegerField(default=0)
	money = models.IntegerField(default=0)
	avatar = models.ImageField(upload_to="Avatars", blank=True)
	subs = models.ManyToManyField(User, default=[], related_name="subs_to", blank=True)
	achievements = models.ManyToManyField(Achievement, default=[], related_name="achieve_owner", blank=True)
	passed_courses = models.ManyToManyField(Articles, default=[], blank=True)
	activity = models.TextField(default='{}')
	skills = models.TextField(default='{}')
	inventory = models.ManyToManyField(GameItems, default=[], related_name="item_owner", blank=True)
	active_frame = models.ForeignKey(GameItems, on_delete=models.SET_NULL, related_name="set_frame",
										blank=True, null=True, default=None)
	active_back = models.ForeignKey(GameItems, on_delete=models.SET_NULL, related_name="set_backs",
										blank=True, null=True, default=None)

	class Meta:
		verbose_name = 'данные пользователя'
		verbose_name_plural = 'данные пользователей'

	def __str__(self):
		return self.user.username


class Post(models.Model):
	title = models.CharField(max_length=100)
	image = models.ImageField(upload_to='Post', blank=True)
	date = models.DateTimeField(auto_now_add=True)
	text = models.TextField()

	class Meta:
		ordering = ('-date', )
		verbose_name = 'пост'
		verbose_name_plural = 'посты'

	def __str__(self):
		return self.title

