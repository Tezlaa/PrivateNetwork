from django.db.models.fields.files import ImageFieldFile
from django.core.exceptions import ValidationError


def get_path_to_upload_avatar(instance, filename: str) -> str:
    return f'avatars/{instance.username}/{filename}'


def validate_size_image(file_obj: ImageFieldFile) -> None:
    """ Validate image by limit of megabytes. """
    limit_megabyte = 5
    if file_obj.size > limit_megabyte * 1024 * 1024:
        raise ValidationError(f'Limite by megabytes. Maximum megabytes - {limit_megabyte}MB')