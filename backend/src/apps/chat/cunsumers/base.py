import json
from typing import Any

from channels.generic.websocket import AsyncWebsocketConsumer

from asgiref.sync import sync_to_async

from apps.lobby.services.model_services import get_lobby
from apps.chat.services.utils import receive_json_to_needed_fields


class ConsumerBase(AsyncWebsocketConsumer):
    """
    Base class for creating a handy cunsumer. Simplifies receiving and sending by websocket group
    
    Atributes:
        available_receive_fields(tuple[str]): required fields for cunsumer
        Example: available_receive_fields = ('type', 'message') => means that the 'type' and 'message' fields
            will be required and each request to the websocket class will check it their are available
    
    Methods:
        `ConsumerBase.sendint_to_group`
    
    Usage requirements:
        1. Create mathod with the name: receive_{incomming request type}(self, fields: dict[str, Any])
            Example:
                # message it`s incomming request type.
                async def receive_message(self, fields: dict[str, Any]):
                    # your business logic.
                    
                    # send_to_group(...) can be found: `ConsumerBase.sendint_to_group`.
        
    """
    
    available_receive_fields = ()
       
    async def sendint_to_group(self, group_name: str, event_method_name: str, sending_data: dict[str, Any]):
        """
        Args:
            group_name(str): the name to send in
            event_method_name(str): the name of event method
            sending_data(dict): fields that will be handler in the event method.
                                You can modify them or add new fields.
        
        Usage example:
            await self.sendint_to_group(
                group_name=self.lobby_group_name,
                event_method_name='chat_message',
                sending_data={
                    'timestamp': int(time()),
                    **fields
                }
            )
        """
        sending_data['type'] = event_method_name
        await self.channel_layer.group_send(  # type: ignore
            group_name, sending_data
        )
    
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
        fields = receive_json_to_needed_fields(text_data_json, self.available_receive_fields)
        receive_type = fields.get('type')
        
        if receive_type is not None:
            await self._search_needed_recieve_method(method=receive_type, fields=fields)
    
    async def _search_needed_recieve_method(self, method: str, fields: dict[str, Any]) -> None:
        method = self.__getattribute__(f'receive_{method}')
        await method(fields)  # type: ignore
