from typing import Optional

from django.db.models import QuerySet, OuterRef, Exists
from django.contrib.auth.models import User

from apps.lobby.models import Lobby

from apps.base.exceptions import OwnerError, UserLimitError, LobbyNotFound
from apps.base.decorators import api_validation_error, banchmark_queries


def is_user_owner(user: User, lobby: Lobby) -> bool:
    return lobby.owners.filter(username=user.username).exists()


def get_user_lobbies(user: User) -> QuerySet[Lobby]:
    return Lobby.objects.filter(user_connected__in=[user]).annotate(
        owner=Exists(User.objects.filter(pk=OuterRef('owners__pk'), username=user.username))
    )


@api_validation_error
def add_user_to_lobby(user: User, lobby: Lobby) -> Lobby:
    user_limit = lobby.user_limit
    
    if user_limit < lobby.user_connected.count() + 1:
        raise UserLimitError(user_limit)
    lobby.user_connected.add(user)
    
    return lobby


@api_validation_error
def add_user_to_lobby_as_owner(user: User, lobby: Lobby) -> Lobby:
    lobby.owners.add(user)
    return add_user_to_lobby(user=user, lobby=lobby)


def remove_user_from_lobby(user: User, lobby: Lobby) -> None:
    user_exists_in_lobby = lobby.user_connected.filter(username=user.username).exists()
    user_owner = is_user_owner(user, lobby)
    
    if user_exists_in_lobby:
        lobby.user_connected.remove(user)
    if user_owner:
        lobby.owners.remove(user)


@api_validation_error
def delete_lobby(user: User, lobby_name: str) -> None:
    lobby = get_lobby(lobby_name=lobby_name, user=user)
    
    if not is_user_owner(user, lobby):
        raise OwnerError

    lobby.delete()
    

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


@api_validation_error
def create_lobby_by_serializer(valid_serializer, user) -> Lobby:
    
    lobby = valid_serializer.save()
    add_user_to_lobby_as_owner(user=user, lobby=lobby)
    
    return lobby