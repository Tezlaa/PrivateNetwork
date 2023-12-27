from django.urls import path

from apps.chat.cunsumers.chat_consumer import ChatConsumerLobby, ChatConsumerContact
from apps.chat.cunsumers.notify_consumer import NotifyConsumer


websocket_urlpatterns = [
    path('ws/chat/lobby/<str:lobby_name>', ChatConsumerLobby.as_asgi()),
    path('ws/chat/contact/<str:contact_id>', ChatConsumerContact.as_asgi()),
    path('ws/notify/', NotifyConsumer.as_asgi()),
]