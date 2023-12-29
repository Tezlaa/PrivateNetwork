from rest_framework import serializers

from apps.chat.models import Message

from apps.accounts.serializers import UserSerializer


class RecursiveField(serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_liked = UserSerializer(many=True)
    reply = RecursiveField(many=True)
    
    class Meta:
        model = Message
        fields = '__all__'