from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def dating(reqeust):
	"""Домашняя страница"""
	return render(reqeust, 'dating_app/dating.html')