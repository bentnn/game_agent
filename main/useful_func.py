from .const import first_level
import re
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


def get_achieve(request, achieve_name):
	about_user = AboutUser.objects.get(user=request.user)
	if len(about_user.achievements.filter(name=achieve_name)) == 0:
		achievement = Achievement.objects.filter(name=achieve_name)
		if len(achievement) != 0:
			about_user.achievements.add(achievement.first())
			messages.success(request,
							 f"вы заработали достижение '{achieve_name}'")
