from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class ObtainAuthStatus(APIView):
    permission_classes = (IsAuthenticated, )
    
    def get(self, request: Request, *args, **kwargs) -> Response:
        """ Obtain auth status """
        
        return Response({'detail': 'Welcome!'}, status=status.HTTP_200_OK)