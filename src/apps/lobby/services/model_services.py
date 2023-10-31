from typing import Optional

from django.db.models import QuerySet
from django.contrib.auth.models import User

from apps.lobby.models import Lobby

from apps.base.exceptions import UserLimitError, LobbyNotFound, api_validation_error


def get_user_lobbies(user: User) -> QuerySet[Lobby]:
    return Lobby.objects.filter(user_connected__in=[user])


@api_validation_error
def add_user_to_lobby(user, lobby: Lobby) -> Lobby:
    user_limit = lobby.user_limit
    
    if user_limit < lobby.user_connected.count() + 1:
        raise UserLimitError(user_limit)
    
    lobby.user_connected.add(user)
    return lobby


def remove_user_from_lobby(user, lobby: Lobby) -> None:
    user_exists_in_lobby = lobby.user_connected.filter(username=user.username).exists()
    user_owner = lobby.owners.filter(username=user.username).exists()
    
    if user_exists_in_lobby:
        lobby.user_connected.remove(user)
    if user_owner:
        lobby.owners.remove(user)


@api_validation_error
def get_lobby(lobby_name: str,
              password: Optional[int] = None,
              user: Optional[User] = None) -> Lobby:
    
    filters = {'lobby_name': lobby_name}
    if password is not None:
        filters['password'] = password  # type: ignore
    if user is not None:
        filters['user_connected__in'] = [user]  # type: ignore
        
    lobby = Lobby.objects.filter(**filters).first()
    
    if lobby is None:
        raise LobbyNotFound(lobby_name)
    
    return lobby


def create_lobby(valid_serializer, user) -> Lobby:
    
    lobby = valid_serializer.save()
    lobby.owners.add(user)
    add_user_to_lobby(user=user, lobby=lobby)
    
    return lobby