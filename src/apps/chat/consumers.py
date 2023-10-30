import json

from channels.generic.websocket import AsyncWebsocketConsumer

from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.scope)
        await self.accept()
    
    async def disconnect(self, close_code):
        print('disconnect')