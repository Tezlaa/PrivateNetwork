from django.db import models

from apps.accounts.models import User


class Message(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    message = models.TextField(verbose_name='Message', max_length=500)
    user_liked = models.ManyToManyField(to=User, blank=True, related_name='liked')
    created_at = models.DateTimeField(verbose_name='created at', auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.user.username}: {self.message[:5]}...'