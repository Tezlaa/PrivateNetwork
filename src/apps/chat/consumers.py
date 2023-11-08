from datetime import datetime
import json

from channels.generic.websocket import AsyncWebsocketConsumer

from django.utils.timesince import timesince

from asgiref.sync import sync_to_async
from apps.chat.services.model_services import send_message

from apps.lobby.services.model_services import get_lobby


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.lobby_name: str = self.scope['url_route']['kwargs'].get('lobby_name', '')
        self.lobby_group_name = f'lobby_{self.lobby_name.replace(" ", "_")}'
        self.lobby = await sync_to_async(get_lobby)(lobby_name=self.lobby_name)
        
        await self.channel_layer.group_add(self.lobby_group_name, self.channel_name)  # type: ignore
        
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.lobby_group_name, self.channel_name)  # type: ignore
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        recieve_type = text_data_json.get('type')
        message = text_data_json.get('message')
        name = text_data_json.get('name')
        
        if recieve_type == 'message':
            new_message = await sync_to_async(send_message)(self.lobby, message, name)
            timestamp = int(round(new_message.created_at.timestamp()))
            
            await self.channel_layer.group_send(  # type: ignore
                self.lobby_group_name, {
                    'type': 'chat_message',
                    'message': message,
                    'name': name,
                    'timestamp': timestamp,
                }
            )
    
    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps({
                'type': event.get('type'),
                'message': event.get('message'),
                'name': event.get('name'),
                'timestamp': event.get('timestamp')
            })
        )