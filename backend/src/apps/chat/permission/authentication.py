from typing import Any, Optional

from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.authentication import JWTAuthentication, AuthUser

from apps.chat.permission.exceptions import HeadersIsEmpty, TokenNotBeFound


class WSJWTAuthentication(JWTAuthentication):
    AUTH_HEADER_NAME_WEBSOCKET = "WS_AUTHORIZATION"
    
    def authenticate(self, scope: dict[str, Any]) -> Optional[tuple[AuthUser, Token]]:
        raw_token = self.get_header(scope)
        
        validated_token = self.get_validated_token(raw_token)
        
        return self.get_user(validated_token), validated_token
    
    def get_header(self, scope: dict[str, Any]) -> bytes:
        headers = scope.get('headers')
        if not headers:
            raise HeadersIsEmpty
        
        auth_header = headers.get(self.AUTH_HEADER_NAME_WEBSOCKET)
        if not auth_header:
            raise TokenNotBeFound
            
        return auth_header