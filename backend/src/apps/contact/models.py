from django.db import models

from apps.chat.models import Message
from apps.accounts.models import User


class Contact(models.Model):
    connect = models.ManyToManyField(to=User, related_name='contact_users', blank=True)
    chat = models.ManyToManyField(to=Message, related_name='contact_messages', blank=True)
    
    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        
    def __str__(self) -> str:
        return ', '.join(user.username for user in self.connect.all())