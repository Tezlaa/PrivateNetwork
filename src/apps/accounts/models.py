from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.contrib.auth.hashers import make_password

from apps.accounts.services.model_service import get_path_to_upload_avatar, validate_size_image


class User(AbstractUser):
    username = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=128)
    
    avatar = models.ImageField(
        verbose_name='Avatar',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'png',],
                message='File type error'
            ),
            validate_size_image
        ],
        upload_to=get_path_to_upload_avatar,
        default=None,
        blank=True,
        null=True,
    )
    
    class Meta(AbstractUser.Meta):
        abstract = False
        verbose_name = 'User'
        verbose_name_plural = 'Users'
     
    def save(self, *args, **kwargs):
        if kwargs.get('force_insert', False):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f'<{self.username}>'