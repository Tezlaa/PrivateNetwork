from django.urls import path

from apps.chat.cunsumers.chat_consumer import ChatConsumer


websocket_urlpatterns = [
    path('ws/chat/<str:lobby_name>', ChatConsumer.as_asgi()),
]