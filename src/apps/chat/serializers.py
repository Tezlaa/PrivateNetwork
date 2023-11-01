from rest_framework import serializers

from apps.chat.models import Message

from apps.account.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_liked = UserSerializer(many=True)
    
    class Meta:
        model = Message
        fields = '__all__'