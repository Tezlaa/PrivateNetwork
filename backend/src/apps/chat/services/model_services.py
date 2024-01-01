from django.shortcuts import get_object_or_404

from apps.chat.models import Message
from apps.contact.models import Contact

from apps.lobby.models import Lobby

from apps.accounts.models import User


def send_message_by_username(lobby: Lobby | Contact, message: str, username: str) -> Message:
    user = get_object_or_404(User, username=username)
    return send_message(lobby, message, user)


def send_message(lobby: Lobby | Contact, message: str, user: User):
    message_inctance = Message.objects.create(
        user=user,
        message=message
    )
    
    lobby.chat.add(message_inctance)
    lobby.save()
    
    return message_inctance
    

def like_for_message(lobby: Lobby | Contact, message_pk: int, username: str, create: bool = True) -> None:
    user = get_object_or_404(User, username=username)
    message = get_object_or_404(lobby.chat, pk=message_pk)

    if create:
        message.user_liked.add(user)
    else:
        message.user_liked.remove(user)
        
    message.save()