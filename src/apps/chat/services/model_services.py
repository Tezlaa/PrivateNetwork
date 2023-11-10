from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from apps.chat.models import Message
from apps.lobby.models import Lobby


def send_message(lobby: Lobby, message: str, username: str) -> Message:
    user = get_object_or_404(User, username=username)
    message_inctance = Message.objects.create(
        user=user,
        message=message
    )
    
    lobby.chat.add(message_inctance)
    lobby.save()
    
    return message_inctance


# TODO: query optimization
def create_like_for_message(lobby: Lobby, message_pk: int, username: str) -> None:
    user = get_object_or_404(User, username=username)
    message = lobby.chat.filter(pk=message_pk).first()
    if message is not None:
        message.user_liked.add(user)
        message.save()
