from django.urls import path
from . import views

app_name = 'dating_app'

urlpatterns = [
    path('', views.dating, name='dating'),
    
    path('search/', views.search_results, name='search_results'),
    path('likes/add/<int:user_id>/', views.like_add, name='like_add'),
    # Профиль другого пользователя
    path('<int:user_id>/', views.partner_account, name='partner_account'),
]