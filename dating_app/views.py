from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime


@login_required
def dating(request):
	"""Домашняя страница"""
	profiles = User.objects.order_by('-last_login')
	date_now = datetime.now()
	return render(request, 'dating_app/dating.html', {'profiles':profiles, 'date_now':date_now})