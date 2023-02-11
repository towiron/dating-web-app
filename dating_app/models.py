from django.db import models
from django.contrib.auth.models import User


class Like(models.Model):
	user = models.ForeignKey(to=User, on_delete=models.CASCADE)
	liked = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked')
	date = models.DateTimeField(auto_now_add=True)	