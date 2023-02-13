from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import UserUpdateForm, ProfileUpdateForm, SignUpStepOneForm, SignUpStepTwoForm, SignUpStepThreeForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from dating_app.models import Favorite

def signup(request):
	"""Регистрация пользователя"""
	if request.user.is_authenticated: # Если пользователь в системе, то у него нет доступа к форме входа
		return redirect('dating_app:dating')
	else:
		error_contex = []
		if request.method == 'GET':
			return render(request, 'user_app/sign_up.html', {'form': UserCreationForm})
		else:
			if not(request.POST['username']):
				error_contex.append('Login can\'t be empty')
			elif not(request.POST['password1']):
				error_contex.append('Password can\'t be empty')
			elif not(request.POST['password2']):
				error_contex.append('Confirm Password can\'t be empty')
			elif request.POST['password1'] != request.POST['password2']:
				error_contex.append('Password did not match')
			elif len(request.POST['password1']) < 8:
				error_contex.append('Password less then 8 characters')
			elif str(request.POST['username']).lower() in ['admin', 'админ', 'аdmin', 'god', 'administrator', 'аdministrator', 'аdministrаtor']:
				error_contex.append('This login can\'t be taken')
			else:
				try:
					user = User.objects.create_user(username = request.POST['username'], password=request.POST['password1'])
					user.save()
					login(request, user)
					return redirect('user_app:sign_up_step_one')
				except IntegrityError:
					error_contex.append('That username has already been taken')
					return render(request, 'user_app/sign_up.html', {'form': UserCreationForm(), 'error_contex': error_contex})	
			return render(request, 'user_app/sign_up.html', {'form': UserCreationForm(), 'error_contex': error_contex})



def signin(request):
	"""Вход пользователя"""
	if request.user.is_authenticated: # Если пользователь в системе, то у него нет доступа к форме входа
		return redirect('dating_app:dating')
	else:
		if request.method == 'GET':
			return render(request, 'user_app/sign_in.html',
										{'form': AuthenticationForm()})
		else:
			user = authenticate(request,username=request.POST['username'],
										password=request.POST['password'])
			if user is None:
				return render(request, 'user_app/sign_in.html',
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
	profile = Profile.objects.get(pk=request.user.pk)
	if profile.about:
		"""Личный аккаунт пользователя, где он может редактировать пользовательские данные"""
		if request.method == 'POST':
			u_form = UserUpdateForm(request.POST, instance=request.user)
			p_form = ProfileUpdateForm(request.POST,
										request.FILES,
										instance=request.user.profile)
			if int(request.POST['age']) < 18:
				return render(request, 'user_app/user_account.html', {'error':'Your age must be at least 18 years old'})
			elif not str(request.POST['age']).isnumeric():
				return render(request, 'user_app/user_account.html', {'error':'Uncorrect age field'})
			else:
				try:
					u_form.save()
					p_form.save()
					return redirect('user_app:user_account') # Перенаправление на страницу профиля пользователя
				except ValueError:
					return render(request, 'user_app/user_account.html', {'error':'Files is too large, requirement is less than 2.5 MB'})

		else:
			u_form = UserUpdateForm(instance=request.user)
			p_form = ProfileUpdateForm(instance=request.user.profile)

		context = {
			'u_form': u_form,
			'p_form': p_form,
			'favorites': Favorite.objects.filter(user=request.user).order_by('-saved_date')
		}

		return render(request, 'user_app/user_account.html', context)
	
	return redirect('user_app:sign_up_step_three')


@login_required
def sign_up_step_one(request):
	if request.method == 'POST':
		step_one_form = SignUpStepOneForm(request.POST,
									request.FILES,
									instance=request.user.profile)
		if not(request.POST['first_name']):
			return render(request, 'user_app/sign_up_step_one.html', {'error': 'First name can\'t be empty'})
		if not(str(request.POST['first_name']).isalpha()):
			return render(request, 'user_app/sign_up_step_one.html', {'error': 'First name can\'t have numbers'})
		elif not(request.POST['last_name']):
			return render(request, 'user_app/sign_up_step_one.html', {'error': 'Last name can\'t be empty'})
		if not(str(request.POST['last_name']).isalpha()):
			return render(request, 'user_app/sign_up_step_one.html', {'error': 'Last name can\'t have numbers'})
		elif not(request.POST['age']):
			return render(request, 'user_app/sign_up_step_one.html', {'error': 'Age can\'t be empty'})
		elif int(request.POST['age']) < 18:
			return render(request, 'user_app/sign_up_step_one.html', {'error': 'Your age must be at least 18 years old'})
		elif not str(request.POST['age']).isnumeric():
				return render(request, 'user_app/sign_up_step_one.html', {'error':'Uncorrect age field'})
		else:
			step_one_form.save()
			return redirect('user_app:sign_up_step_two')
	else:
		step_one_form = SignUpStepOneForm(instance=request.user.profile)

	context = {
		'step_one_form': step_one_form,
	}
	return render(request, 'user_app/sign_up_step_one.html', context)



@login_required
def sign_up_step_two(request):
	profile = Profile.objects.get(pk=request.user.pk)
	if profile.first_name and profile.last_name and profile.age:
		if request.method == 'POST':
			step_two_form = SignUpStepTwoForm(request.POST,
										request.FILES,
										instance=request.user.profile)
			if not(request.POST['city']):
				return render(request, 'user_app/sign_up_step_two.html', {'error': 'Location can\'t be empty'})
			elif request.POST['sex'] not in ['M', 'F']:
					return render(request, 'user_app/sign_up_step_two.html', {'error': 'Choose correct sex field'})
			elif request.POST['seeking'] not in ['M', 'F']:
					return render(request, 'user_app/sign_up_step_two.html', {'error': 'Choose correct seeking field'})
			else:
				step_two_form.save()
				return redirect('user_app:sign_up_step_three')
		else:
			step_two_form = SignUpStepTwoForm(instance=request.user.profile)

		context = {
			'step_two_form': step_two_form,
		}
		return render(request, 'user_app/sign_up_step_two.html', context)
	return redirect('user_app:sign_up_step_one')


@login_required
def sign_up_step_three(request):
	profile = Profile.objects.get(pk=request.user.pk)
	if profile.city and profile.sex and profile.seeking:
		if request.method == 'POST':
			step_three_form = SignUpStepThreeForm(request.POST,
										request.FILES,
										instance=request.user.profile)
			if not(request.POST['about']):
				return render(request, 'user_app/sign_up_step_three.html', {'error': 'About field can\'t be empty'})
			else:
				try:
					step_three_form.save()
					return redirect('dating_app:dating')
				except ValueError:
					return render(request, 'user_app/sign_up_step_three.html', {'error': 'File is too large, requirement is less than 2.5 MB'})

		else:
			step_three_form = SignUpStepThreeForm(instance=request.user.profile)

		context = {
			'step_three_form': step_three_form,
		}
		return render(request, 'user_app/sign_up_step_three.html', context)
	return redirect('user_app:sign_up_step_two')