from django.urls import path

from apps.chat.cunsumers.chat_consumer import ChatConsumer
from apps.chat.cunsumers.notify_consumer import NotifyConsumer


websocket_urlpatterns = [
    path('ws/chat/<str:lobby_name>', ChatConsumer.as_asgi()),
    path('ws/notify/', NotifyConsumer.as_asgi()),
]