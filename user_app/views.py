from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

def auth_user(request):
	if request.user.is_authenticated:
		return redirect('dating_app:profile_info')
	else:
		return render(request, 'user_app/auth_user.html')


def signup(request):
	"""Регистрация пользователя"""
	if request.method == 'GET':
		return render(request, 'user_app/auth_user.html', {'form': UserCreationForm})
	else:
		if not(request.POST['username']):
			return render(request, 'user_app/auth_user.html', {'form':UserCreationForm(), 'error':'Login can\'t be empty'})
		elif not(request.POST['password1']):
			return render(request, 'user_app/auth_user.html', {'form':UserCreationForm(), 'error':'Password can\'t be empty'})
		elif not(request.POST['password2']):
			return render(request, 'user_app/auth_user.html', {'form':UserCreationForm(), 'error':'Confirm Password can\'t be empty'})
		elif request.POST['password1'] != request.POST['password2']:
			return render(request, 'user_app/auth_user.html', {'form':UserCreationForm(), 'error':'Password did not match'})
		elif len(request.POST['password1']) < 8:
			return render(request, 'user_app/auth_user.html', {'form':UserCreationForm(), 'error':'Password less then 8 characters'})
		elif len(request.POST['username']) < 5:
			return render(request, 'user_app/auth_user.html', {'form':UserCreationForm(), 'error':'Login less then 5 characters'})
		else:
			try:
				user = User.objects.create_user(username = request.POST['username'], password=request.POST['password1'])
				user.save()
				login(request, user)
				return redirect('user_app:profile_info')
			except IntegrityError:
					return render(request, 'user_app/auth_user.html', {'form': UserCreationForm(), 'error': '*That username has already been taken'})	

@login_required		
def profile_info(request):
	profile = Profile.objects.get(pk=request.user.pk)
	if not profile.first_name:	
		"""Личный аккаунт пользователя, где он может редактировать пользовательские данные"""
		if request.method == 'POST':
			p_form = ProfileUpdateForm(request.POST,
										request.FILES,
										instance=request.user.profile)
			if p_form.is_valid():
				p_form.save()
				messages.success(request, f'Your account has been updated!')
				return redirect('dating_app:dating') # Перенаправление на страницу профиля пользователя
		else:
			p_form = ProfileUpdateForm(instance=request.user.profile)

		context = {
			'p_form': p_form,
		}

		return render(request, 'user_app/profile_info.html', context)
	else:
		return redirect('dating_app:dating')



def signin(request):
	"""Вход пользователя"""
	if request.user.is_authenticated: # Если пользователь в системе, то у него нет доступа к форме входа
		return redirect('dating_app:profile_info')
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
				return redirect('user_app:profile_info')


@login_required
def logout_user(request):
	"""Выход пользователя из системы"""
	if request.method == 'POST':
		logout(request)
		return redirect('user_app:signin')


@login_required
def user_account(request):
	profile = Profile.objects.get(pk=request.user.pk)
	if profile.first_name:
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
	
	else:
		return redirect('user_app:profile_info')
