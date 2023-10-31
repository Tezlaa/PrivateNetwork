from django.db import QuerySet

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from apps.lobby.models import Lobby
from apps.lobby.serializers import LobbySerializer, LobbyJoinSerializer
from apps.lobby.services.model_services import (
    get_lobby, get_user_lobby, add_user_to_lobby, create_lobby
)


class LobbyGenericAPIView(GenericAPIView):
    serializer_class = None
    permission_classes = (IsAuthenticated, )

    def serialize_inctance_to_dict(self,
                                   inctance: QuerySet[Lobby] | Lobby,
                                   many: bool = False) -> dict:
        return LobbySerializer(inctance=inctance, many=many).data

    def get_queryset(self):
        return Lobby.objects.all()


class GetLobbies(LobbyGenericAPIView):
    serializer_class = LobbySerializer
    
    def get(self, request):
        """ Get all the user`s lobbies. """
        user_lobby = get_user_lobby(request.user)
        serializer_data = self.get_serializer(instance=user_lobby, many=True).data
        return Response(serializer_data)


class CreateLobby(LobbyGenericAPIView):
    serializer_class = LobbySerializer
    
    def post(self, request):
        """ Create lobby. """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lobby = create_lobby(valid_serializer=serializer, user=request.user)
        
        return Response(self.serialize_inctance_to_dict(lobby))


class ConnectDisconnectFromLobby(LobbyGenericAPIView):
    serializer_class = LobbyJoinSerializer
    lobby_serializer = LobbySerializer
    
    def post(self, request, lobby_name: str):
        """ Join to lobby by password and lobby name. """
        user = request.user
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        lobby = get_lobby(lobby_name=lobby_name, password=serializer.data.get('password'))
        add_user_to_lobby(user, lobby)
        
        return Response(self.serialize_inctance_to_dict(lobby))
        
    def delete(self, request, lobby_name: str):
        """ Disconnect from lobby. """
        
        