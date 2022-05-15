import matplotlib.pyplot as plt
from io import StringIO, BytesIO
import re
import base64
import json
import urllib
import datetime
import json
import numpy as np
from .const import skills
from .useful_func import convert_fig_or_pil_to_img


def create_activity():
	data = {}
	minimum = datetime.date.today() - datetime.timedelta(9)
	for i in range(10):
		data[str(minimum + datetime.timedelta(i))] = 0
	return data


def norm_activity(data):
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
	last = data.popitem()
	last[1] += activity
	data[last[0]] = last[1]
	return data


# def show_activity(data, name, data2=None, name2=None):
def show_activity(*args):
	args_len = len(args)
	if args_len < 2:
		raise ValueError(f"Количество аргументов для графика активности "
						 f"{args_len}, а должно быть 2 или 4")
	data, name = args[0], args[1]
	data2, name2 = None, None
	if args_len == 4:
		data2, name2 = args[2], args[3]
	if isinstance(data, str):
		data = json.loads(data)

	x = []
	y = []
	fig, ax = plt.subplots()
	for i in data.items():
		x.append(str(i[0])[5:])
		y.append(i[1])

	ax.plot(x, y, label=name)

	if data2 is not None:
		if isinstance(data2, str):
			data2 = json.loads(data2)
		y2 = []
		for i in data2.values():
			y2.append(i)
		ax.plot(x, y2, label=name2)

	ax.legend(loc='upper left')
	plt.grid()
	return convert_fig_or_pil_to_img(plt.gcf())


def create_skills():
	return dict.fromkeys(skills, 0)


def show_skills(data):
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
	plt.ylim(0, 40)
	plt.yticks(color='gray')
	plt.fill(color='b')
	lines, labels = plt.thetagrids(np.degrees(label_loc), labels=categories)

	# imgdata = BytesIO()
	# plt.savefig(imgdata, format='svg', transparent=True)
	# imgdata.seek(0)
	# string = base64.b64encode(imgdata.read())
	# uri = urllib.parse.quote(string)
	# return uri

	# fig = plt.gcf()
	# #convert graph into dtring buffer and then we convert 64 bit code into image
	# buf = BytesIO()
	# fig.savefig(buf, format='png')
	# buf.seek(0)
	# string = base64.b64encode(buf.read())
	# uri = urllib.parse.quote(string)
	# return uri
	return convert_fig_or_pil_to_img(plt.gcf())
