from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime


@login_required
def dating(request):
	"""Домашняя страница"""
	profiles = User.objects.order_by('-last_login')
	date_now = datetime.now()
	return render(request, 'dating_app/dating.html', {'profiles':profiles, 'date_now':date_now})


@login_required
def partner_account(request, user_id):
	"""Показ деталей профилья других пользователей"""
	partner_account = get_object_or_404(User, pk=user_id)
	return render(request, 'dating_app/partner_account.html', {'partner_account':partner_account})


def home(request):
	return redirect('dating_app:dating')


def search_results(request):
	search = str(request.GET.get('search'))
	profiles = User.objects.order_by('-last_login')
	return render(request, 'dating_app/search_results.html', {'search': search, 'profiles':profiles})