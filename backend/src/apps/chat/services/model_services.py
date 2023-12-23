from django.shortcuts import get_object_or_404

from apps.chat.models import Message

from apps.lobby.models import Lobby

from apps.accounts.models import User


def send_message(lobby: Lobby, message: str, username: str) -> Message:
    user = get_object_or_404(User, username=username)
    message_inctance = Message.objects.create(
        user=user,
        message=message
    )
    
    lobby.chat.add(message_inctance)
    lobby.save()
    
    return message_inctance


def like_for_message(lobby: Lobby, message_pk: int, username: str, create: bool = True) -> None:
    user = get_object_or_404(User, username=username)
    message = get_object_or_404(lobby.chat, pk=message_pk)

    if create:
        message.user_liked.add(user)
    else:
        message.user_liked.remove(user)
        
    message.save()