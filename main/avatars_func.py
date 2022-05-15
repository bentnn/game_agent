import numpy as np
import hashlib
from PIL import ImageDraw, Image


def get_basic_avatar(username):

	background_color = '#f2f1f2'
	bytes = hashlib.md5(username.encode('utf-8')).digest()
	main_color = bytes[:3]
	main_color = tuple(channel // 2 + 128 for channel in main_color) # rgb
	need_color = np.array([bit == '1' for byte in bytes[3:3+9] for bit in bin(byte)[2:].zfill(8)]).reshape(6, 12)

	# получаем матрицу 12 на 12 сконкатенировав оригинальную и отраженную матрицу
	need_color = np.concatenate((need_color, need_color[::-1]), axis=0)
	avatar_size = 1200
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
	crop_size = min(pil_img.size)
	return crop_center(pil_img, crop_size, crop_size)
