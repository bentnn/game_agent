import matplotlib.pyplot as plt
from io import StringIO, BytesIO
import re
import base64
import json
import urllib
from .models import AboutUser
from course.models import Articles
import datetime
import json
import numpy as np
from .const import skills
from .useful_func import convert_fig_or_pil_to_img, add_exp
from django.contrib import messages


def create_activity():
	data = {}
	minimum = datetime.date.today() - datetime.timedelta(9)
	for i in range(10):
		data[str(minimum + datetime.timedelta(i))] = 0
	return data


def norm_activity(data: dict or str):
	if isinstance(data, str):
		data = json.loads(data)
	today = datetime.date.today()
	minimum = today - datetime.timedelta(9)
	for i in list(data.items()):
		if datetime.datetime.strptime(i[0], '%Y-%m-%d').date() < minimum:
			data.pop(i[0])
	for i in range(10 - len(data)):
		data[str(today - datetime.timedelta(i))] = 0
	return dict(sorted(data.items()))


def add_activity(data: dict, activity):
	data[datetime.date.today().strftime('%Y-%m-%d')] += activity
	# last = data.popitem()
	# last[1] += activity
	# data[last[0]] = last[1]
	return data


def get_activity(about_user: AboutUser):
	data = norm_activity(about_user.activity)
	about_user.activity = json.dumps(data)
	about_user.save()
	return data


def show_activity(*args):
	args_len = len(args)
	if args_len < 2:
		raise ValueError(f"Количество аргументов для графика активности "
						 f"{args_len}, а должно быть 2 или 4")
	data, name = args[0], args[1]
	if isinstance(data, str):
		data = json.loads(data)

	fig, ax = plt.subplots()
	x = [str(date)[5:] for date in data.keys()]

	ax.plot(x, data.values(), label=name)
	max_y = max(data.values())
	if args_len == 4:
		data2, name2 = args[2], args[3]
		if isinstance(data2, str):
			data2 = json.loads(data2)
		ax.plot(x, data2.values(), label=name2)
		max_y = max(*data2.values(), max_y)

	ax.legend(loc='upper left')
	if max_y < 20:
		plt.ylim(-0.5, 20)
	else:
		plt.ylim(-0.5)
	plt.grid()
	res = convert_fig_or_pil_to_img(plt.gcf())
	plt.close(fig)
	return res


def create_skills():
	return dict.fromkeys(skills, 0)


def show_skills(data: dict or str):
	if isinstance(data, str):
		data = json.loads(data)
	categories = list(data.keys())
	categories = [*categories, categories[0]]

	values = list(data.values())
	values = [*values, values[0]]

	label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(values))

	plt.figure(figsize=(8, 8))
	ax = plt.subplot(polar=True)
	plt.plot(label_loc, values)
	plt.title('skills', size=20, y=1.05)
	plt.ylim(0, 200)
	plt.yticks(color='gray')
	plt.fill(color='b')
	lines, labels = plt.thetagrids(np.degrees(label_loc), labels=categories)

	return convert_fig_or_pil_to_img(plt.gcf())


def give_reward(about_user: AboutUser, article: Articles, request=None):
	if not article.reward:
		return
	reward = json.loads(article.reward)
	skills = json.loads(about_user.skills)
	activity = norm_activity(about_user.activity)
	exp_sum = 0

	for theme, exp in reward.items():
		if theme in skills:
			skills[theme] += exp
			exp_sum += exp

	activity = add_activity(activity, exp_sum)
	about_user.skills = json.dumps(skills)
	about_user.activity = json.dumps(activity)
	about_user.save()

	if request:
		messages.success(request, f"Здорово! Ты заработал очки опыта: " + ", ".join(f'{name} - {exp}' for name, exp in reward.items()))
	add_exp(about_user, exp_sum, request)
