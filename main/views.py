from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import Group, User
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import *
from .useful_func import get_basic_avatar, get_needed_exp
import logging

# set logger level
logging.basicConfig(level=logging.DEBUG)


def about_us(request):
	return render(request, "about_us.html")


@login_required(login_url='login')
def home(request):
	return render(request, 'home.html', {"posts": Post.objects.all()[:5]})


def login_view(request):
	er_message = None
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
				er_message = "Пользователь не найден"
		else:
			er_message = "Форма невалидна"
	else:
		form = AuthenticationForm()
	return render(request, 'login.html', {'form': form, 'er_message': er_message})


def check_in_view(request):
	er_message = None
	if request.method == 'POST':
		form = UserCreationForm(data=request.POST)
		if form.is_valid():
			username = request.POST['username']
			if username.isascii():
				password = request.POST['password1']
				form.save()
				user = authenticate(username=username, password=password)
				get_basic_avatar(username).save(f"media/Avatars/{username}.jpg")
				AboutUser.objects.create(user=user, avatar=f"Avatars/{username}.jpg")
				login(request, user)
				return redirect('home')
			else:
				er_message = "Имя пользователя может состоять только из латинских букв," \
								" цифр и специальных символов"
		else:
			er_message = "Форма невалидна"
	else:
		form = UserCreationForm()
	return render(request, 'check_in.html', {'form': form, 'er_message': er_message})


@login_required(login_url='login')
def logout_view(request):
	logout(request)
	return redirect('login')


def error_404(request, exception):
	return render(request, '404.html', status=404)


@login_required(login_url='login')
def profile(request, username, action=None):
	# user = User.objects.get(username=username)
	user = get_object_or_404(User, username=username)
	if user is None or user.is_superuser:
		logging.info(f"404: User <{username}> was not founded")
		return error_404(request, 404)
	logging.info(f"User <{username}> was found")
	about_user = AboutUser.objects.get(user=user)
	about_request = about_user if request.user == user else AboutUser.objects.get(user=request.user)
	about_user.achievements.add(Achievement.objects.all()[0])
	# print(list(about_user.achievements.all()))
	# about_user.save()
	# print([i.user.username for i in request.user.subs_to.all()])
	if request.user != user and action is not None:
		if action == "sub":
			about_request.subs.add(user)
			about_request.save()
		elif action == "unsub":
			about_request.subs.remove(user)
			about_request.save()

	return render(
		request, 'profile.html',
		{
			"user": user,
			"about_user": about_user,
			"to_next_level": round(about_user.exp_to_level / get_needed_exp(about_user.level + 1), 2),
			"subs": list(about_user.subs.all()),
			"subs_to": list(user.subs_to.all()),
			"req_subs": list(about_request.subs.all()),
			"achievements": list(about_user.achievements.all())
		}
	)


@login_required(login_url='login')
def change_profile(request):
	er_msg = None
	if request.method == "POST":
		data = list()
		# about_user = AboutUser.objects.get(user=request.user)
		for i in ["username", "email"]:
			data.append(request.POST[i])
		# avatar = request.POST['username']
		if all(i for i in data) and data[0].isascii():
			request.user.username = data[0]
			request.user.email = data[1]
			request.user.save()
		else:
			er_msg = "Некорректные данные"
	return render(request, "change_profile.html", {"er_msg": er_msg})
