from django.shortcuts import render

def dating(reqeust):
	"""Домашняя страница"""
	return render(reqeust, 'dating_app/dating.html')