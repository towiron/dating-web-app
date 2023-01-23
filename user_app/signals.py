from django.db.models.signals import post_save # Импортируется сигнал post_save при создании пользователя
from django.contrib.auth.models import User # Импортируется встроенная модель User, которая является отправителем
from django.dispatch import receiver # Импорт приемника
from .models import Profile # Модель профиля


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
