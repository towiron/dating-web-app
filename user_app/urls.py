from django.urls import path
from . import views

app_name = 'user_app'

urlpatterns = [
	# Аутентификация
    path('signup/', views.signup, name='signup'),
	path('signin/', views.signin, name='signin'),
	path('logout/', views.logout_user, name='logout_user'),
	path('profile_info/', views.profile_info, name='profile_info'),

	# Страница пользователя
	path('user_account/', views.user_account, name='user_account'),
]