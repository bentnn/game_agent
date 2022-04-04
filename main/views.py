from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import Group, User
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import *
from .useful_func import get_basic_avatar


def about_us(request):
	return render(request, "about_us.html")


def home(request):
	if not request.user.is_authenticated:
		return redirect('about_us')
	return render(request, 'home.html')


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
def profile(request, username):
	user = User.objects.get(username=username)
	if user is None:
		return error_404(request, 404)
	about_user = AboutUser.objects.get(user=user)
	print(about_user.avatar.url)
	return render(
		request, 'profile.html',
		{
			'user': user,
			"about_user": about_user
		}
	)
