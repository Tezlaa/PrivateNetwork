import json
from typing import Any
from asgiref.sync import sync_to_async

from apps.chat.services.model_services import like_for_message, send_message_by_username
from apps.chat.cunsumers.base import ConsumerBase
from apps.lobby.services.model_services import get_lobby
from apps.contact.services.model_services import get_contact_instance_by_his_id


class ChatConsumerLobby(ConsumerBase):
    available_receive_fields = ('type', 'message', 'username', 'message_id')
    
    async def preconnect(self) -> str:
        self.lobby_indentical: str = self.scope['url_route']['kwargs'].get('lobby_name', '')
        self.lobby = await sync_to_async(get_lobby)(lobby_name=self.lobby_indentical)

        return f'lobby_{self.lobby_indentical.replace(" ", "_")}'
    
    async def receive_message(self, fields: dict[str, Any]) -> None:
        new_message = await sync_to_async(send_message_by_username)(self.lobby, fields['message'], fields['username'])

        await self.sendint_to_group(group_name=self.group_name,
                                    event_method_name='chat_message',
                                    sending_data={
                                        'timestamp': int(round(new_message.created_at.timestamp())),
                                        'message_id': new_message.pk,
                                        **fields,
                                    })

    async def receive_delete_like(self, fields: dict[str, Any]) -> None:
        await sync_to_async(like_for_message)(self.lobby, fields['message_id'], fields['username'], False)
        
        await self.sendint_to_group(group_name=self.group_name,
                                    event_method_name='chat_delete_like',
                                    sending_data={
                                        **fields,
                                    })
    
    async def receive_like(self, fields: dict[str, Any]) -> None:
        await sync_to_async(like_for_message)(self.lobby, fields['message_id'], fields['username'])
        
        await self.sendint_to_group(group_name=self.group_name,
                                    event_method_name='chat_like',
                                    sending_data={
                                        **fields,
                                    })
    
    async def chat_like(self, event):
        await self.send(
            text_data=json.dumps({
                'type': event.get('type'),
                'message_id': event.get('message_id'),
                'username': event.get('username'),
            })
        )
        
    async def chat_delete_like(self, event):
        await self.chat_like(event)
    
    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps({
                'type': event.get('type'),
                'message': event.get('message'),
                'username': event.get('username'),
                'message_id': event.get('message_id'),
                'timestamp': event.get('timestamp'),
            })
        )


class ChatConsumerContact(ChatConsumerLobby):
    async def preconnect(self) -> str:
        self.contact_id: str = self.scope['url_route']['kwargs'].get('contact_id', '')
        self.lobby = await sync_to_async(get_contact_instance_by_his_id)(contact_id=int(self.contact_id))

        return f'lobby_{self.contact_id.replace(" ", "_")}'