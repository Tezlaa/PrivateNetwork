from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_str

from rest_framework.exceptions import APIException
from rest_framework import status


class UserLimitError(APIException):
    status_code = status.HTTP_501_NOT_IMPLEMENTED
    default_detail = _('Out of limit users {limit}.')
    default_code = 'Out of limit users'
    
    def __init__(self, limit: int, detail=None, code=None):
        detail = force_str(self.default_detail.format(limit=limit))
        
        super().__init__(detail, code)
        

class LobbyNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('Lobby "{lobby_name}" not found in the database or password doesn`t match.')
    default_code = 'Lobby not found'
    
    def __init__(self, lobby_name: str, detail=None, code=None):
        detail = force_str(self.default_detail.format(lobby_name=lobby_name))
        
        super().__init__(detail, code)
        

class OwnerError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('You are not the owner of this lobby.')
    default_code = 'Not the owner'