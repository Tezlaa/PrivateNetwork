from rest_framework import serializers

from apps.accounts.serializers import UserSerializerByUsername
from apps.chat.serializers import MessageSerializer
from apps.contact.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    connect = UserSerializerByUsername(many=True)
    messages = MessageSerializer(many=True, read_only=True, source='chat')
    connect_user = serializers.CharField(required=False)
    
    class Meta:
        model = Contact
        fields = ('id', 'connect', 'messages', 'connect_user')