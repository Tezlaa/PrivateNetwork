from datetime import datetime
import json
from typing import Any

from channels.generic.websocket import AsyncWebsocketConsumer

from django.utils.timesince import timesince

from asgiref.sync import sync_to_async
from apps.chat.services.model_services import send_message
from apps.chat.services.utils import receive_json_to_needed_fields

from apps.lobby.services.model_services import get_lobby


class ChatConsumer(AsyncWebsocketConsumer):
    receive_fields = ('type', 'message', 'name')
       
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
        fields = receive_json_to_needed_fields(text_data_json, self.receive_fields)
        receive_type = fields.get('type')
        
        if receive_type is not None:
            await self.search_needed_recieve_method(method=receive_type, fields=fields)
    
    async def search_needed_recieve_method(self, method: str, fields: dict[str, Any]) -> None:
        method = self.__getattribute__(f'receive_{method}')
        await method(fields)  # type: ignore
    
    async def receive_message(self, fields: dict[str, Any]) -> None:
        new_message = await sync_to_async(send_message)(self.lobby, fields['message'], fields['name'])
        
        await self.sendint_to_group(group_name=self.lobby_group_name, send_type='chat_message', sending_data={
            **fields,
            'timestamp': int(round(new_message.created_at.timestamp())),
        })

    async def receive_like(self, fields: dict[str, Any]) -> None:
       await sync_to_async()
    
    async def sendint_to_group(self, group_name: str, send_type: str, sending_data: dict[str, Any]):
        sending_data['type'] = send_type
        await self.channel_layer.group_send(  # type: ignore
            group_name, sending_data
        )
    
    async def chat_like(self, event):
        await self.send(
            text_data=json.dumps({
                'type': event.get('type'),
                'message_pk': event.get('message_pk'),
                'name': event.get('name'),
            })
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