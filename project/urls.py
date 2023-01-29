from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from dating_app import views

urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),

    path('admin/', admin.site.urls),
    path('dating/', include('dating_app.urls')), # Основная страница
    path('', views.home, name='home'), # Корневой страница которая редиректиться на dating/
    path('', include('user_app.urls')), # Авторизация
    path('chat/', include('chat_app.urls')), # Чат
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)