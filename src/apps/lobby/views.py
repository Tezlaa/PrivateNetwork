from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from apps.lobby.models import Lobby
from apps.lobby.serializers import LobbySerializer
from apps.lobby.services.model_services import (
    get_user_lobby, add_user_to_lobby
)


class LobbyReceiveCreate(GenericAPIView):
    serializer_class = LobbySerializer
    queryset = Lobby.objects.all()
    permission_classes = (IsAuthenticated, )
    
    def get(self, request):
        """ Get all the user`s lobbies """
        user_lobby = get_user_lobby(request.user)
        serializer_data = self.get_serializer(instance=user_lobby, many=True).data
        return Response(serializer_data)
    
    def post(self, request):
        """ Create lobby """
        user = request.user
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lobby = serializer.save()
        
        lobby.owner.add(user)
        add_user_to_lobby(user=user, lobby=lobby)
        
        serializer_data = self.get_serializer(instance=lobby).data
        return Response(serializer_data)
    

class LobbyActions(GenericAPIView):
    serializer_class = LobbySerializer
    queryset = Lobby.objects.all()
    permission_classes = (IsAuthenticated, )
    
    def post(self, request, lobby_name: str):
        pass