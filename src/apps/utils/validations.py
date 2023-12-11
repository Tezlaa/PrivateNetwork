from django.core.exceptions import ValidationError


def validate_password(value: int):
    password_lenght = len(str(value))
    if password_lenght < 4:
        raise ValidationError(f'The password length must be greater than 4. {password_lenght} < 4')