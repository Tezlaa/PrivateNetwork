from rest_framework.exceptions import ValidationError


def api_validation_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise ValidationError(e)
    return wrapper


class UserLimitError(Exception):
    def __init__(self, limit: int) -> None:
        super().__init__(f'Out of limit in {limit} user!')