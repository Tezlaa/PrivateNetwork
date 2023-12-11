from django.contrib.auth.models import User

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from apps.account.serializers import UserSerializer


class UserRegister(GenericAPIView):
    serializer_class = UserSerializer
    
    def post(self, request: Request, *args, **kwargs):
        """ Api for register user """
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        return User.objects.all()
    