from django.db import models
from django.contrib.auth.models import User

from apps.chat.models import Message


class Lobby(models.Model):
    lobby_name = models.CharField(verbose_name='Lobby name', max_length=50, unique=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Lobby owner')
    password = models.IntegerField(verbose_name='Password')
    user_limit = models.IntegerField(verbose_name='User limit', default=2)
    user_connected = models.ManyToManyField(to=User,
                                            verbose_name='User connected', 
                                            related_name='user_connected')
    chat = models.ManyToManyField(to=Message, related_name='messages', blank=True)
    
    class Meta:
        verbose_name = 'Lobby'
        verbose_name_plural = 'Lobby'
        
    def is_limit(self) -> bool:
        if self.user_connected.count() >= self.user_limit:
            return False
        return True