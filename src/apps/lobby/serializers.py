from rest_framework import serializers

from apps.chat.serializers import MessageSerializer
from apps.lobby.models import Lobby
from apps.account.serializers import UserSerializer


class LobbySerializer(serializers.ModelSerializer):
    user_connected = UserSerializer(read_only=True, many=True)
    owner = UserSerializer(read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source='chat')
    
    class Meta:
        model = Lobby
        fields = ('lobby_name', 'password', 'owner',
                  'user_limit', 'user_connected', 'messages')
        extra_kwargs = {
            'password': {'write_only': True}
        }