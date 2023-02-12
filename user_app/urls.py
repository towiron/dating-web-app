from django.urls import path
from . import views

app_name = 'user_app'

urlpatterns = [
	# Аутентификация
    path('signup/', views.signup, name='signup'),
	path('signin/', views.signin, name='signin'),
	path('logout/', views.logout_user, name='logout_user'),
	path('signup/step_one/', views.sign_up_step_one, name='sign_up_step_one'),
	path('signup/step_two/', views.sign_up_step_two, name='sign_up_step_two'),
	path('signup/step_three/', views.sign_up_step_three, name='sign_up_step_three'),

	# Страница пользователя
	path('user_account/', views.user_account, name='user_account'),
]