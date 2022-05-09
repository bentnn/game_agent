from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import (
	AuthenticationForm,
	PasswordChangeForm,
	UserCreationForm,
	PasswordResetForm
)
from fuzzywuzzy import fuzz
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import logging
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from .const import domain
from .models import *
from .useful_func import *
from .avatars_func import *
from .activity_func import *


logger = logging.getLogger("Agent")
logger.setLevel(logging.DEBUG)


def about_us(request):
	return render(request, "about_us.html")


@login_required(login_url='login')
def home(request):
	return render(request, 'home.html', {"posts": Post.objects.all()[:5]})


@login_required(login_url='login')
def post_view(request, id):
	post = get_object_or_404(Post, id=id)
	return render(request, 'post_page.html', {'post': post})


def login_view(request):
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.error(request, "Пользователь не найден")
		else:
			messages.error(request, "Форма невалидна")
	else:
		form = AuthenticationForm()
	return render(request, 'login.html', {'form': form})


def check_in_view(request):
	if request.method == 'POST':
		form = UserCreationForm(data=request.POST)
		if form.is_valid():
			username = request.POST['username']
			if is_ascii(username):
				password = request.POST['password1']
				form.save()
				user = authenticate(username=username, password=password)
				get_basic_avatar(username).save(f"{settings.MEDIA_ROOT}/Avatars/{username}.jpg")
				AboutUser.objects.create(
					user=user,
					avatar=f"Avatars/{username}.jpg",
					activity=json.dumps(create_activity()),
					skills=json.dumps(create_skills())
				)
				login(request, user)
				messages.success(request,
								 "Ваш аккаунт успешно создан. Перейдите в "
								 "профиль->настройки, чтобы ввести электронную "
								 "почту. Она понадобится, "
								 "если вы вдруг забудете пароль.")
				return redirect('home')
			else:
				messages.error(request, "Имя пользователя может состоять "
										"только из латинских букв, "
										"цифр и специальных символов")
		else:
			messages.error(request, "Форма невалидна")
	else:
		form = UserCreationForm()
	return render(request, 'check_in.html', {'form': form})


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(email=data)
			if associated_users.exists():
				for user in associated_users:
					text = f"""
					http://{domain}/reset/{urlsafe_base64_encode(force_bytes(user.pk))}/{default_token_generator.make_token(user)}/
					"""
					send_mail(data, text)
					return redirect("/password_reset/done/")
			else:
				messages.error(request, "Мы не нашли подходящего пользователя")
		else:
			messages.error(request, "Форма невалидна")
	password_reset_form = PasswordResetForm()
	return render(request, "reset_pswrd/password_reset.html",
					{"password_reset_form": password_reset_form}
	)


@login_required(login_url='login')
def logout_view(request):
	logout(request)
	return redirect('login')


def error_404(request, exception):
	return render(request, '404.html', status=404)


@login_required(login_url='login')
def users_action(request, username, action=None):
	user = get_object_or_404(User, username=username)
	about_request = AboutUser.objects.get(user=request.user)

	if request.user != user and action is not None:
		if action == "sub":
			about_request.subs.add(user)
			about_request.save()
		elif action == "unsub":
			about_request.subs.remove(user)
			about_request.save()

		if len(about_request.achievements.filter(name='socialization')) == 0:
			get_achieve(request, 'socialization')

	return redirect('profile', username)


@login_required(login_url='login')
def profile(request, username):
	user = get_object_or_404(User, username=username)
	if user is None or user.is_superuser:
		return error_404(request, 404)
	about_user = AboutUser.objects.get(user=user)
	about_request = about_user if request.user == user else AboutUser.objects.get(user=request.user)

	# рисуем активность
	data = norm_activity(about_user.activity)
	about_user.activity = json.dumps(data)
	about_user.save()
	activity_data = [data, user.username]
	if user != request.user:
		req_data = norm_activity(about_request.activity)
		about_request.activity = json.dumps(req_data)
		about_request.save()
		activity_data = [req_data, request.user.username, *activity_data]
	graph = show_activity(*activity_data)

	return render(
		request, 'profile.html',
		{
			"user": user,
			"about_user": about_user,
			"to_next_level": round(about_user.exp_to_level / get_needed_exp(about_user.level + 1), 2),
			"subs": list(about_user.subs.all()),
			"subs_to": list(user.subs_to.all()),
			"req_subs": list(about_request.subs.all()),
			"achievements": list(about_user.achievements.all()),
			"activity": graph,
			"skills": show_skills(about_user.skills),
			"avatar": frame_layering(about_user.avatar, about_user.active_frame)
		}
	)


@login_required(login_url='login')
def inventory(request, username):
	user = get_object_or_404(User, username=username)
	about_user = AboutUser.objects.get(user=user)
	return render(
		request, "inventory.html",
		{
			"about_user": about_user,
			"frames": about_user.inventory.filter(type='fr'),
			"backs": about_user.inventory.filter(type='bg'),
			"avatar": frame_layering(about_user.avatar, about_user.active_frame)
		}
	)


@login_required(login_url='login')
def set_item(request, id):
	"""
	:param id: 100000 -> null frame, 200000 - null back
	"""
	about_request = AboutUser.objects.get(user=request.user)
	if id == 100000:
		about_request.active_frame = None
	elif id == 200000:
		about_request.active_back = None
	else:
		item = get_object_or_404(GameItems, id=id)
		if len(about_request.inventory.filter(id=item.id)) == 0:
			return error_404(request, None)

		if item.type == 'fr':
			about_request.active_frame = item
		elif item.type == 'bg':
			about_request.active_back = item

	about_request.save()
	return redirect("inventory", request.user.username)


@login_required(login_url='login')
def game_shop(request):
	about_request = AboutUser.objects.get(user=request.user)
	invent = list(about_request.inventory.all())
	frames = filter(lambda x: x not in invent,
					GameItems.objects.filter(type='fr'))
	backs = filter(lambda x: x not in invent,
					GameItems.objects.filter(type='bg'))
	return render(
		request, 'shop.html',
		{
			'about_user': about_request,
			'inventory': invent,
			'frames': frames,
			'backs': backs,
		}
	)


@login_required(login_url='login')
def buy_item(request, id):
	about_request = AboutUser.objects.get(user=request.user)
	item = get_object_or_404(GameItems, id=id)
	if len(about_request.inventory.filter(id=item.id)) != 0:
		messages.error(request, "У вас уже есть данный айтем")
	elif item.price > about_request.money:
		messages.error(request, "У вас недостаточно игровой валюты")
	else:
		about_request.money -= item.price
		about_request.inventory.add(item)
		about_request.save()
	return game_shop(request)


@login_required(login_url='login')
def change_profile(request):
	about_user = AboutUser.objects.get(user=request.user)
	if request.method == "POST":
		try:
			for i in ['username', 'first_name', 'last_name', 'email']:
				set_change(request, i)

			data = request.FILES.get("avatar")
			if data is not None:
				filename = f"Avatars/{request.user.username}.png"
				full_filename = str(settings.MEDIA_ROOT) + '/' + filename
				with open(full_filename, 'wb') as f:
					f.write(data.read())
				im = Image.open(full_filename)
				im = crop_max_square(im)
				im.save(full_filename, quality=95)
				about_user.avatar = filename
				about_user.save()

			request.user.save()
			messages.success(request, "Изменения успешно внесены")
		except ValueError as e:
			messages.error(request, f"{e}")
	return render(request, "change_profile.html", {"about_user": about_user})


@login_required(login_url='login')
def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			messages.error(request, "Ваш пароль был успешно изменен")
		else:
			messages.error(request, "Форма смены пароля невалидна")
	else:
		form = PasswordChangeForm(request.user)
	return render(request, 'change_password.html', {'form': form})


def search_user(request):
	res = None
	if request.method == 'POST':
		username = request.POST.get('username')
		users = User.objects.all()
		res = [i for i in users if fuzz.ratio(i.username, username) > 70]
		if len(res) == 0:
			messages.warning(request, f"Пользователь '{username}' не найден")
	return render(request, 'search_user.html', {'users': res})
