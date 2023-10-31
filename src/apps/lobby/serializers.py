from rest_framework import serializers

from apps.chat.serializers import MessageSerializer

from apps.lobby.models import Lobby

from apps.account.serializers import UserSerializer


class LobbySerializer(serializers.ModelSerializer):
    owners = UserSerializer(read_only=True, many=True)
    user_connected = UserSerializer(read_only=True, many=True)
    messages = MessageSerializer(many=True, read_only=True, source='chat')
    
    class Meta:
        model = Lobby
        fields = ('lobby_name', 'password', 'owners',
                  'user_limit', 'user_connected', 'messages')
        extra_kwargs = {
            'password': {'write_only': True},
        }


class LobbySerializerOnlyNames(serializers.ModelSerializer):
    user_connected = serializers.SerializerMethodField()
    
    class Meta:
        model = Lobby
        fields = ('lobby_name', 'user_connected')
    
    def get_user_connected(self, obj) -> int:
        return obj.user_connected.count()


class LobbyJoinSerializer(serializers.Serializer):
    password = serializers.IntegerField()