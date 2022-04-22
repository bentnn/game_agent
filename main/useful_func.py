from PIL import ImageDraw, Image
from .const import first_level
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO
import hashlib
import re
import json
import datetime


def get_basic_avatar(username):

	background_color = '#f2f1f2'
	bytes = hashlib.md5(username.encode('utf-8')).digest()
	main_color = bytes[:3]
	main_color = tuple(channel // 2 + 128 for channel in main_color) # rgb
	need_color = np.array([bit == '1' for byte in bytes[3:3+9] for bit in bin(byte)[2:].zfill(8)]).reshape(6, 12)

	# получаем матрицу 12 на 12 сконкатенировав оригинальную и отраженную матрицу
	need_color = np.concatenate((need_color, need_color[::-1]), axis=0)
	avatar_size = 120
	img_size = (avatar_size, avatar_size)
	block_size = avatar_size // 12 # размер квадрата

	img = Image.new('RGB', img_size, background_color)
	draw = ImageDraw.Draw(img)

	for x in range(avatar_size):
		for y in range(avatar_size):
			need_to_paint = need_color[x // block_size, y // block_size]
			if need_to_paint:
				draw.point((x, y), main_color)

	return img


def get_needed_exp(level):
	if level < 1 or not isinstance(level, int):
		raise ValueError("Неверный формат уровня")
	if level == 1:
		return first_level
	return round(first_level * 1.15**(level - 1))


def email_is_valid(email: str):
	# regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
	regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
	return re.fullmatch(regex, email)


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
		if datetime.date.fromisoformat(i[0]) < minimum:
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
	imgdata = StringIO()
	plt.savefig(imgdata, format='svg', transparent=True)
	imgdata.seek(0)
	return imgdata.getvalue()


def crop_center(pil_img, crop_width: int, crop_height: int) -> Image:
	"""
	Функция для обрезки изображения по центру.
	"""
	img_width, img_height = pil_img.size
	return pil_img.crop((
				(img_width - crop_width) // 2,
                (img_height - crop_height) // 2,
                (img_width + crop_width) // 2,
                (img_height + crop_height) // 2)
	)


def crop_max_square(pil_img):
	return crop_center(pil_img, min(pil_img.size), min(pil_img.size))