from django.urls import path, include
from . import views

app_name = 'dating_app'

urlpatterns = [
    path('', views.home, name='home')
]