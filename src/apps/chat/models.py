from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    message = models.TextField(verbose_name='Message', max_length=500)
    user_liked = models.ManyToManyField(to=User, blank=True, related_name='liked')