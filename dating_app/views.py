from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from user_app.models import Profile
from django.db.models import Q
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.views.generic import ListView, DetailView



@login_required
def dating(request):
	"""Домашняя страница"""
	profiles_list = User.objects.all()
	profiles_list = User.objects.exclude(id=request.user.id)
	contex = get_pogination(request, profiles_list, 10)
	date_now = datetime.now()
	contex.update({'date_now': date_now})
	return render(request, 'dating_app/dating.html', contex)


@login_required
def partner_account(request, user_id):
	"""Показ деталей профилья других пользователей"""
	partner_account = get_object_or_404(User, pk=user_id)
	return render(request, 'dating_app/partner_account.html', {'partner_account':partner_account})


@login_required
def home(request):
	return redirect('dating_app:dating')


@login_required
def search_results(request):
	"""Поиск пользователей"""
	query = request.GET.get("q", default = "")
	
	profiles_list = Profile.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
	contex = get_pogination(request, profiles_list, 10)
	if profiles_list:
		contex.update({'query': f'We found {len(profiles_list)} people with name "{query}"'})
	else:
		contex.update({'query': f'There are no people with name "{query}"'})
	return render(request, 'dating_app/search.html', contex)


def get_pogination(request, profiles_list, objects_num):
	"""Пагинация"""
	paginator = Paginator(profiles_list.order_by('-last_login'), objects_num)
	try:
		page = int(request.GET.get('page', '1'))
	except:
		page = 1
	
	try:
		profiles = paginator.page(page)
	except(EmptyPage, InvalidPage):
		profiles = paginator.page(paginator.num_pages)
	page_range = paginator.get_elided_page_range(number=page)

	contex = {
		'profiles':profiles,
		'page_range': page_range
	}
	return contex
