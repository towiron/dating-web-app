from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.models import User
from .models import Message
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from dating_app.models import Favorite


class MessagesListView(LoginRequiredMixin, ListView):
	"""Входящие/сообщения/список пользователей"""
	model = Message
	template_name = 'chat_app/messages_list.html'
	# контекстные данные для отображения последнего сообщения
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = User.objects.get(pk=self.request.user.pk)  # получение вашего первичного ключа
		messages = Message.get_message_list(user) # получение всех сообщений между вами и другим пользователем

		other_users = [] # список других пользователей

		# получение имени другого человека из списка сообщений и добавление его в список
		for i in range(len(messages)):
			if messages[i].sender != user:
				other_users.append(messages[i].sender)
			else:
				other_users.append(messages[i].recipient)


		context['messages_list'] = messages
		context['other_users'] = other_users
		context['user'] = user
		context['favorites'] = Favorite.objects.filter(user=self.request.user).order_by('-saved_date')
		return context


class InboxView(LoginRequiredMixin, DetailView):
	"""Просмотр чата"""
	model = Message
	template_name = 'chat_app/inbox.html'
	queryset = User.objects.all()


	# для отправки сообщения (передайте имя пользователя вместо первичного ключа в функцию post)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(self.request, *args, **kwargs)

	# заменять запрос по умолчанию в detailview на запрос pk или slug, чтобы вместо этого получить имя пользователя
	def get_object(self):
		UserName= self.kwargs.get("username")
		return get_object_or_404(User, username=UserName)



	# контекстные данные для представления чата
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = User.objects.get(pk=self.request.user.pk)  # получение вашего первичного ключа
		other_user = User.objects.get(username=self.kwargs.get("username"))  # получение первичного ключа других пользователей
		messages = Message.get_message_list(user) # получать все сообщения между вами и другим пользователем

		other_users = [] # список других пользователей

		# получение имени другого человека из списка сообщений и добавление его в список
		for i in range(len(messages)):
			if messages[i].sender != user:
				other_users.append(messages[i].sender)
			else:
				other_users.append(messages[i].recipient)

		sender = other_user  # отправителем сообщения будет получателем самого последнего сообщения после его отправки
		recipient = user # получателем сообщения будет отправитель самого последнего сообщения после его отправки

		context['messages'] = Message.get_all_messages(sender, recipient)  # получить все сообщения между отправителем (вами) и получателем (другим пользователем)
		context['messages_list'] = messages # для шаблона MessagesListView
		context['other_person'] = other_user  # узнайте имя другого человека, с которым вы общаетесь, из указанного имени пользователя
		context['user'] = user  # отправьте свой основной ключ на POST
		context['other_users'] = other_users
		context['favorites'] = Favorite.objects.filter(user=self.request.user).order_by('-saved_date')

		return context

    # Отправить сообщение
	def post(self, request, *args, **kwargs):
		# print("sender: ", request.POST.get("user"))
		# print("recipient: ", request.POST.get('recipient'))
		sender = User.objects.get(pk=request.POST.get('user'))  # узнать отправителя сообщения (человека, который его отправил)
		recipient = User.objects.get(pk=request.POST.get('recipient'))  # получить получателя сообщения (Вас)
		message = request.POST.get('message')  # получить сообщение из формы

		# если отправитель вошел в систему, отправить сообщение
		if request.user.is_authenticated:
			if request.method == 'POST':
				if message:
					Message.objects.create(sender=sender, recipient=recipient, message=message)
			return redirect('chat_app:inbox', username=recipient.username)  # перенаправление в папку входящих сообщений получателя

		else:
			# return render(request, 'auth/login.html')
			pass

class UserListsView(LoginRequiredMixin, ListView):
	"""Список пользователей"""
	model = User
	template_name = 'chat_app/users_list.html'
	context_object_name = 'users'

	# контекстные данные для списка пользователей
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = User.objects.get(pk=self.request.user.pk)  # получение вашего первичного ключа
		context['users'] = User.objects.exclude(pk=user.pk)  # получить доступ ко всем пользователям, кроме вас
		return context



class ChatView(LoginRequiredMixin, DetailView):
	"""Просмотр чата"""
	model = Message
	template_name = 'chat_app/chat.html'
	queryset = User.objects.all()


	# для отправки сообщения (передайте имя пользователя вместо первичного ключа в функцию post)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(self.request, *args, **kwargs)

	# заменять запрос по умолчанию в detailview на запрос pk или slug, чтобы вместо этого получить имя пользователя
	def get_object(self):
		UserName= self.kwargs.get("username")
		return get_object_or_404(User, username=UserName)



	# контекстные данные для представления чата
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = User.objects.get(pk=self.request.user.pk)  # получение вашего первичного ключа
		other_user = User.objects.get(username=self.kwargs.get("username"))  # получение первичного ключа других пользователей
		messages = Message.get_message_list(user) # получать все сообщения между вами и другим пользователем

		other_users = [] # список других пользователей

		# получение имени другого человека из списка сообщений и добавление его в список
		for i in range(len(messages)):
			if messages[i].sender != user:
				other_users.append(messages[i].sender)
			else:
				other_users.append(messages[i].recipient)

		sender = other_user  # отправителем сообщения будет получателем самого последнего сообщения после его отправки
		recipient = user # получателем сообщения будет отправитель самого последнего сообщения после его отправки

		context['messages'] = Message.get_all_messages(sender, recipient)  # получить все сообщения между отправителем (вами) и получателем (другим пользователем)
		context['messages_list'] = messages # для шаблона MessagesListView
		context['other_person'] = other_user  # узнайте имя другого человека, с которым вы общаетесь, из указанного имени пользователя
		context['user'] = user  # отправьте свой основной ключ на POST
		context['other_users'] = other_users
		context['favorites'] = Favorite.objects.filter(user=self.request.user).order_by('-saved_date')

		return context

    # Отправить сообщение
	def post(self, request, *args, **kwargs):
		# print("sender: ", request.POST.get("user"))
		# print("recipient: ", request.POST.get('recipient'))
		sender = User.objects.get(pk=request.POST.get('user'))  # узнать отправителя сообщения (человека, который его отправил)
		recipient = User.objects.get(pk=request.POST.get('recipient'))  # получить получателя сообщения (Вас)
		message = request.POST.get('message')  # получить сообщение из формы

		# если отправитель вошел в систему, отправить сообщение
		if request.user.is_authenticated:
			if request.method == 'POST':
				if message:
					Message.objects.create(sender=sender, recipient=recipient, message=message)
			return redirect('chat_app:message_list', username=recipient.username)  # перенаправление в папку входящих сообщений получателя

		else:
			# return render(request, 'auth/login.html')
			pass