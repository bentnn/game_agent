from .const import first_level
import re
import json
from PIL import Image
from io import BytesIO
import urllib
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib.auth.models import User
from .models import AboutUser, Achievement
from django.contrib import messages


def is_ascii(s):
	return all(ord(c) < 128 for c in s)


def get_needed_exp(level: int):
	"""

	:param level: уровень, для которого рассчитывается нужный опыт
	:return: необходимый для набора данного уровня опыт
	"""
	if not isinstance(level, int) or level < 1:
		raise ValueError("Неверный формат уровня")
	return first_level if level == 1\
		else round(first_level * 1.15**(level - 1))


def add_exp(about_user: AboutUser, exp: int, request=None):
	about_user.exp_to_level += exp
	needed_exp = get_needed_exp(about_user.level + 1)
	if about_user.exp_to_level >= needed_exp:
		about_user.exp_to_level -= needed_exp
		about_user.level += 1
		if request:
			messages.success(request, f"Ого! Ты повысил уровень до {about_user.level}!")
	about_user.save()


def email_is_valid(email: str):
	regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
	return re.fullmatch(regex, email)


def send_mail(mail, text):
	addr_from = "programming.agent@yandex.ru"
	password = "ecovachexwuyiiij"

	msg = MIMEMultipart()
	msg['From'] = addr_from
	msg['To'] = mail
	msg['Subject'] = 'Game agent'

	msg.attach(MIMEText(text, 'plain'))
	try:
		server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
		server.login(addr_from, password)
		server.sendmail(addr_from, mail, msg.as_string())
		server.quit()
		return None
	except Exception as e:
		return f"error: {e}"


def convert_fig_or_pil_to_img(fig):
	buf = BytesIO()
	try:
		fig.savefig(buf, format='png')
	except Exception:
		fig.save(buf, "PNG")
	buf.seek(0)
	string = base64.b64encode(buf.read())
	uri = urllib.parse.quote(string)
	return uri


def frame_layering(avatar, frame):
	background = Image.open(avatar)
	if frame is not None:
		foreground = Image.open(frame.image)
		foreground = foreground.resize(background.size)
		background.paste(foreground, (0, 0), foreground)
	return convert_fig_or_pil_to_img(background)


def set_change(request, atr: str):
	data = request.POST.get(atr)
	if getattr(request.user, atr) == data:
		return
	if data is not None:
		if atr == 'username':
			if User.objects.filter(username=data).first():
				raise ValueError(f"Username '{data}' уже занят")
			valid = is_ascii(data)
		elif atr.endswith('_name'):
			valid = any([data.isalpha(), data == ''])
		else:
			valid = any([email_is_valid(data), data == ''])

		if valid:
			request.user.__setattr__(atr, data)
		else:
			raise ValueError(f"{atr} - {data}")
	elif atr == 'username':
		raise ValueError("Username является обязательным полем")


def check_achieve(request):
	about_user = AboutUser.objects.get(user=request.user)
	skills = json.dumps(about_user.skills)
	achievements = list(Achievement.objects.all())
	for i in achievements:
		try:
			if eval(i.condition):
				give_achieve(request, about_user=about_user, achievement=i)
		except Exception as e:
			print(f"Error, can't give achievement '{i.name}': {e}")


def give_achieve(request, **kwargs):
	"""

	:param request: просто реквест
	:param kwargs: achieve_name or achievement
	"""
	about_user = kwargs.get('about_user') or AboutUser.objects.get(user=request.user)
	achievement = kwargs.get('achievement') or Achievement.objects.get(name=kwargs.get('achieve_name'))
	if not about_user.achievements.filter(achievement).exists():
		about_user.achievements.add(achievement)
		messages.success(request,
						 f"вы заработали достижение '{achievement.name}'")
