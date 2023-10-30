from django.db.models import QuerySet

from apps.lobby.models import Lobby

from apps.base.exceptions import UserLimitError, api_validation_error


def get_user_lobby(user) -> QuerySet[Lobby]:
    return Lobby.objects.filter(user_connected__in=[user])


@api_validation_error
def add_user_to_lobby(user, lobby: Lobby) -> Lobby:
    user_limit = lobby.user_limit
    
    if user_limit < user_limit + 1:
        raise UserLimitError(user_limit)
    
    lobby.user_connected.add(user)
    return lobby