from django.urls import path
from . import views

app_name = 'dating_app'

urlpatterns = [
    path('', views.dating, name='dating')
]