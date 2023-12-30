from django.db import models
from django.core.validators import FileExtensionValidator
from django.conf import settings

from apps.accounts.models import User
from apps.chat.services.utils import (
    get_path_for_voice_message, get_path_for_file_message
)


class Message(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    message = models.TextField(verbose_name='Message', max_length=500, null=True, blank=True)
    voice_record = models.FileField(
        upload_to=get_path_for_voice_message,
        validators=[
            FileExtensionValidator(settings.AVAILABLE_AUDIO_FORMATS)
        ],
        null=True, blank=True,
    )
    reply_message = models.ForeignKey(to='self', on_delete=models.SET_NULL, null=True,
                                      blank=True, related_name='reply')
    files = models.ManyToManyField(to='File', blank=True)
    user_liked = models.ManyToManyField(to=User, blank=True, related_name='liked')
    created_at = models.DateTimeField(verbose_name='created at', auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.user.username}: {self.message[:5]}...'
    

class File(models.Model):
    sign = models.CharField(max_length=100, null=True, blank=True, default=None)
    file = models.FileField(
        upload_to=get_path_for_file_message,
        validators=[
            FileExtensionValidator(settings.AVAILABLE_FILE_FORMATS),
        ],
        null=True, blank=True,
    )
    
    def __str__(self) -> str:
        return f'{self.sing}: Path: {self.file}'