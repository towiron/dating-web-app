from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import UserCreateForm
from django.contrib.auth.models import User
from django.db import IntegrityError



def signup(request):
	"""Регистрация пользователя"""
	if request.user.is_authenticated:
		return redirect('dating_app:dating')
	else:
		if request.method == 'GET':
			return render(request, 'user_app/signup.html', {'form': UserCreateForm()})
		else:
			if request.POST['password1'] == request.POST['password2']:
				try:
					user = User.objects.create_user(username = request.POST['username'],
													password=request.POST['password1'])
					user.save()
					login(request, user)
					return redirect('dating_app:dating')
				except IntegrityError:
					return render(request, 'user_app/signup.html',
								{'form': UserCreateForm(),'error': 'That username has already been taken'})
				except ValueError:
					return render(request, 'user_app/signup.html',
								{'form': UserCreateForm(), 'error': 'Need to fill in all the fields'})
			else:
				return render(request, 'user_app/signup.html',
							{'form': UserCreateForm(), 'error': 'Password did not match'})

def signin(request):
	"""Авторизация пользователя"""
	if request.user.is_authenticated:
		return redirect('dating_app:dating')
	else:
		if request.method == 'GET':
			return render(request, 'user_app/signin.html', {'form': AuthenticationForm()})
		else:
			user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
			if user is None:
				return render(request, 'user_app/signin.html', {'form': AuthenticationForm(), 'error':'Username or password did not match'})
			else:
				login(request, user)
				return redirect('dating_app:dating')


@login_required
def logout_user(request):
	"""Выход пользователя из системы"""
	if request.method == 'POST':
		logout(request)
		return redirect('dating_app:dating')

