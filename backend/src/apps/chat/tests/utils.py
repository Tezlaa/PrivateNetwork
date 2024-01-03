
from apps.chat.models import Message
from apps.accounts.models import User

from rest_framework_simplejwt.tokens import AccessToken


def tp_to_unaccurate(json: dict) -> dict:
    """ timestamp to unaccurate format """

    json['timestamp'] = str(json['timestamp'])[:8]
    return json


def isoformat_to_unaccurate(json: dict) -> dict:
    if json.get('created_at', False):
        json['created_at'] = json['created_at'].split('.')[0][:-3]
        
    return json


def get_access_token(user: User) -> str:
    return str(AccessToken.for_user(user))


def delete_temp_files_from_message_instance() -> None:
    Message.objects.first().files.first().file.delete()
    Message.objects.first().voice_record.delete()
    Message.objects.first().delete()