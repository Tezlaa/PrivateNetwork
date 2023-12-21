from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from apps.accounts.serializers import UserSerializer
from apps.accounts.models import User


class UserRegister(GenericAPIView):
    serializer_class = UserSerializer
    
    def post(self, request: Request, *args, **kwargs) -> Response:
        """ Api for register user """
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        return User.objects.all()


class ObtainUserInfo(GenericAPIView):
    serializer_class = UserSerializer
    
    def get(self, request: Request, *args, **kwargs) -> Response:
        """ Api for getting info about user """

        serializer_data = self.get_serializer(instance=request.user).data
        
        return Response(serializer_data, status=status.HTTP_200_OK)

    def get_queryset(self):
        return User.objects.all()