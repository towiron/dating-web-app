from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from user_app.models import Profile
from django.db.models import Q
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from .models import Like



@login_required
def dating(request):
	profile = Profile.objects.get(pk=request.user.pk)
	if profile.first_name:
		"""Домашняя страница"""
		profiles_list = User.objects.order_by('-last_login')
		profiles_list = User.objects.exclude(id=request.user.id)
		contex = get_pogination(request, profiles_list, 10)
		date_now = datetime.now()
		contex.update({'date_now': date_now})
		contex.update({'likes': Like.objects.filter(user=request.user).order_by('-date')})
		return render(request, 'dating_app/dating.html', contex)
	else:
		return redirect('user_app:profile_info')


def like_add(request, user_id):
	liked = User.objects.get(id=user_id)
	likes = Like.objects.filter(user=request.user, liked=liked)

	if not likes.exists():
		Like.objects.create(user=request.user, liked=liked)
	else:
		like = Like.objects.get(liked=liked)
		like.delete()
	return HttpResponseRedirect(request.META['HTTP_REFERER'])




@login_required
def partner_account(request, user_id):
	profile = Profile.objects.get(pk=request.user.pk)
	if profile.first_name:
		"""Показ деталей профилья других пользователей"""
		partner_account = get_object_or_404(User, pk=user_id)
		return render(request, 'dating_app/partner_account.html', {'partner_account':partner_account, 'likes': Like.objects.filter(user=request.user).order_by('-date')})
	else:
		return redirect('user_app:profile_info')


@login_required
def home(request):
	profile = Profile.objects.get(pk=request.user.pk)
	if profile.first_name:
		return redirect('dating_app:dating')
	else:
		return redirect('user_app:profile_info')


@login_required
def search_results(request):
	profile = Profile.objects.get(pk=request.user.pk)
	if profile.first_name:
		"""Поиск пользователей"""
		query = request.GET.get("q", default = "")
		sex = request.GET.get('sex', default = ['M', 'F'])
		if sex == 'ALL':
			sex = ['M', 'F']
		
		profiles_list = Profile.objects.filter(
				Q(first_name__icontains=query) | Q(last_name__icontains=query), sex__in=sex
			).exclude(id=request.user.id)

		contex = get_pogination(request, profiles_list, 10)
		contex.update({'likes': Like.objects.filter(user=request.user).order_by('-date')})
		if profiles_list:
			contex.update({'query': f'We found {len(profiles_list)} people with name "{query}"'})
		else:
			contex.update({'query': f'There are no people with name "{query}"'})
		return render(request, 'dating_app/search.html', contex)
	else:
		return redirect('user_app:profile_info')


def get_pogination(request, profiles_list, objects_num):
	"""Пагинация"""
	paginator = Paginator(profiles_list, objects_num)
	try:
		page = int(request.GET.get('page', '1'))
	except:
		page = 1
	
	try:
		cards = paginator.page(page)
	except(EmptyPage, InvalidPage):
		cards = paginator.page(paginator.num_pages)
	page_range = paginator.get_elided_page_range(number=page)

	contex = {
		'cards':cards,
		'page_range': page_range
	}
	return contex
