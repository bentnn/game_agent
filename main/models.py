from django.db import models
from django.contrib.auth.models import User


class AboutUser(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	level = models.SmallIntegerField(default=0)
	exp_to_level = models.SmallIntegerField(default=0)
	money = models.IntegerField(default=0)
	avatar = models.ImageField(upload_to="Avatars", blank=True)
	subs = models.ManyToManyField(User, default=[], related_name="subs")
