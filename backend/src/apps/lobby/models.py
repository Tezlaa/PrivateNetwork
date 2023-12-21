from django.db import models
from django.core.validators import MinValueValidator

from apps.chat.models import Message

from apps.accounts.models import User

from apps.utils.validations import validate_password


class Lobby(models.Model):
    lobby_name = models.CharField(verbose_name='Lobby name', max_length=50, unique=True)
    owners = models.ManyToManyField(to=User, verbose_name='Lobby owners', blank=True)
    password = models.PositiveIntegerField(verbose_name='Password', default=1111,
                                           validators=[validate_password])
    user_limit = models.PositiveIntegerField(verbose_name='User limit', default=2,
                                             validators=[MinValueValidator(1)])
    user_connected = models.ManyToManyField(to=User,
                                            verbose_name='User connected',
                                            related_name='user_connected',
                                            blank=True)
    chat = models.ManyToManyField(to=Message, related_name='messages', blank=True)
    
    class Meta:
        verbose_name = 'Lobby'
        verbose_name_plural = 'Lobby'
        
    def is_limit(self) -> bool:
        if self.user_connected.count() >= self.user_limit:
            return False
        return True

    def __str__(self) -> str:
        return (
            f'{self.lobby_name}'
        )