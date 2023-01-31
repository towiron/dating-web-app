from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


def auth_user(request):
	return render(request, 'user_app/auth_user.html')


def signup(request):
	"""Регистрация пользователя"""
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("dating_app:dating")
		return render(request, 'user_app/auth_user.html',
								{'form': UserCreationForm(),
								'error': 'Unsuccessful registration. Invalid information.'})
	form = UserCreationForm()
	return render(request, 'user_app/auth_user.html', {'form': UserCreationForm()})

			


	# if request.user.is_authenticated:
	# 	return redirect('dating_app:dating')
	# else:
	# 	if request.method == 'GET':
	# 		return render(request, 'user_app/signup.html', {'form': UserCreationForm()})
	# 	else:
	# 		if request.POST['password1'] == request.POST['password2']:
	# 			try:
	# 				user = User.objects.create_user(username = request.POST['username'],
	# 												password=request.POST['password1'])
	# 				user.save()
	# 				login(request, user)
	# 				return redirect('dating_app:dating')
	# 			# Отлов ошибок
	# 			except IntegrityError:
	# 				return render(request, 'user_app/signup.html',
	# 							{'form': UserCreationForm(),
	# 							'error': 'That username has already been taken'})
	# 			except ValueError:
	# 				return render(request, 'user_app/signup.html',
	# 							{'form': UserCreationForm(),
	# 							'error': 'Need to fill in all the fields'})
	# 		else:
	# 			return render(request, 'user_app/signup.html',
	# 						{'form': UserCreationForm(),
	# 						'error': 'Password did not match'})


def signin(request):
	"""Вход пользователя"""
	if request.user.is_authenticated: # Если пользователь в системе, то у него нет доступа к форме входа
		return redirect('dating_app:dating')
	else:
		if request.method == 'GET':
			return render(request, 'user_app/auth_user.html',
										{'form': AuthenticationForm()})
		else:
			user = authenticate(request,username=request.POST['username'],
										password=request.POST['password'])
			if user is None:
				return render(request, 'user_app/auth_user.html',
							{'form': AuthenticationForm(),
							'error_signin':'Username or password did not match'})
			else:
				login(request, user)
				return redirect('dating_app:dating')


@login_required
def logout_user(request):
	"""Выход пользователя из системы"""
	if request.method == 'POST':
		logout(request)
		return redirect('user_app:signin')


@login_required
def user_account(request):
	"""Личный аккаунт пользователя, где он может редактировать пользовательские данные"""
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST,
									request.FILES,
									instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('user_app:user_account') # Перенаправление на страницу профиля пользователя

	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	context = {
		'u_form': u_form,
		'p_form': p_form,
	}

	return render(request, 'user_app/user_account.html', context)

