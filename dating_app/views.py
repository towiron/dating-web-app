from django.shortcuts import render

def home(reqeust):
	"""Домашняя страница"""
	return render(reqeust, 'dating_app/home.html')