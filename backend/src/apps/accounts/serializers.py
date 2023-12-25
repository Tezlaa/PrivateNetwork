from rest_framework import serializers

from apps.accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'password', 'avatar')
        extra_kwargs = {
            'password': {'write_only': True},
            'avatar': {'read_only': True}
        }


class UserSerializerByUsername(serializers.Serializer):
    username = serializers.CharField()