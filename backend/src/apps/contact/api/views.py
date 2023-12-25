import json

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema

from apps.accounts.models import User
from apps.contact.models import Contact
from apps.contact.serializers import ContactSerializer
from apps.accounts.serializers import UserSerializerByUsername
from apps.contact.services.model_services import create_contact_by_users


class CreateContact(GenericAPIView):
    serializer_class = ContactSerializer
    input_serializer_class = UserSerializerByUsername
    
    @swagger_auto_schema(
        request_body=UserSerializerByUsername,
        responses={201: ContactSerializer}
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        serialize = self.get_input_serializer(data=request.data)
        serialize.is_valid(raise_exception=True)
        searched_username = serialize.data
        
        contact = create_contact_by_users(
            connecting_user=request.user,
            user=User.objects.get(**searched_username)
        )
        return Response(self.get_serializer(instance=contact).data, status=status.HTTP_201_CREATED)
    
    def get_input_serializer(self, *args, **kwargs):
        serializer_class = self.input_serializer_class
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)
    
    def get_queryset(self):
        return Contact.objects.all()