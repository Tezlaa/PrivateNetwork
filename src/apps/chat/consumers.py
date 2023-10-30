import json

from channels.generic.websocket import AsyncWebsocketConsumer

from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.lobby_name = self.scope['url_route']['kwargs'].get('lobby_name')
        self.lobby_group_name = f'lobby_{self.lobby_name}'
        
        await self.channel_layer.group_add(self.lobby_group_name, self.channel_name)
        
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.lobby_group_name, self.channel_name)