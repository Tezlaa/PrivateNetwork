from django.db.models import QuerySet

from apps.lobby.models import Lobby

from apps.base.exceptions import UserLimitError, LobbyNotFound, api_validation_error


def get_user_lobby(user) -> QuerySet[Lobby]:
    return Lobby.objects.filter(user_connected__in=[user])


@api_validation_error
def add_user_to_lobby(user, lobby: Lobby) -> Lobby:
    user_limit = lobby.user_limit
    
    if user_limit < lobby.user_connected.count() + 1:
        raise UserLimitError(user_limit)
    
    lobby.user_connected.add(user)
    return lobby


@api_validation_error
def get_lobby(lobby_name: str, password: int) -> Lobby:
    lobby = Lobby.objects.filter(lobby_name=lobby_name, password=password).first()
    
    if lobby is None:
        raise LobbyNotFound(lobby_name)
    
    return lobby


def create_lobby(valid_serializer, user) -> Lobby:
    
    lobby = valid_serializer.save()
    lobby.owners.add(user)
    add_user_to_lobby(user=user, lobby=lobby)
    
    return lobby