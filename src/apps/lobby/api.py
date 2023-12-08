from attr import s
from django.db.models import QuerySet

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from apps.lobby.models import Lobby
from apps.lobby.serializers import (
    LobbySerializer, LobbyJoinSerializer, LobbySerializerOnlyNames
)
from apps.lobby.services.model_services import (
    get_lobby, get_user_lobbies, add_user_to_lobby, create_lobby_by_serializer, remove_user_from_lobby,
    delete_lobby,
)


class LobbyGenericAPIView(GenericAPIView):
    serializer_class = LobbySerializer
    permission_classes = (IsAuthenticated, )

    def serialize_instance_to_dict(self, instance: QuerySet[Lobby] | Lobby,
                                   many: bool = False) -> dict:
        return LobbySerializer(instance=instance, many=many).data  # type: ignore

    def get_queryset(self):
        return Lobby.objects.all()


class GetLobbies(LobbyGenericAPIView):
    def get(self, request):
        """ Get all the user`s lobbies. """
        
        user_lobby = get_user_lobbies(request.user)
        serializer_data = self.get_serializer(instance=user_lobby, many=True).data
        return Response(serializer_data,
                        status=status.HTTP_200_OK)
        

class GetLobby(LobbyGenericAPIView):
    def get(self, request, lobby_name: str):
        """ Get lobby by his name """
        lobby = get_lobby(lobby_name, user=request.user)
        return Response(self.serialize_instance_to_dict(lobby),
                        status=status.HTTP_200_OK)
        

class GetLobbiesNames(GetLobbies):
    serializer_class = LobbySerializerOnlyNames


class CreateLobby(LobbyGenericAPIView):
    def post(self, request):
        """ Create lobby. """
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lobby = create_lobby_by_serializer(
            valid_serializer=serializer,
            user=request.user
        )
        
        return Response(self.serialize_instance_to_dict(lobby),
                        status=status.HTTP_201_CREATED)


class DeleteLobby(LobbyGenericAPIView):
    def delete(self, request, lobby_name: str):
        """ Delete lobby. """

        delete_lobby(user=request.user, lobby_name=lobby_name)
        
        return Response(status=status.HTTP_204_NO_CONTENT)


class ConnectDisconnectFromLobby(LobbyGenericAPIView):
    serializer_class = LobbyJoinSerializer
    
    def post(self, request, lobby_name: str):
        """ Join to lobby by password and lobby name. """
        
        user = request.user
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        lobby = get_lobby(lobby_name=lobby_name, password=serializer.data.get('password'))
        add_user_to_lobby(user, lobby)
        
        return Response(self.serialize_instance_to_dict(lobby),
                        status=status.HTTP_201_CREATED)
        
    def delete(self, request, lobby_name: str):
        """ Disconnect from lobby. """
        
        lobby = get_lobby(lobby_name, user=request.user)
        remove_user_from_lobby(request.user, lobby)
        
        return Response(status=status.HTTP_204_NO_CONTENT)
        