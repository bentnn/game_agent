from PIL import ImageDraw, Image
from .const import first_level
import numpy as np
import hashlib
import re


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
