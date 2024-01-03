from dataclasses import asdict
import json
from typing import Any
from asgiref.sync import sync_to_async
from apps.chat.services.action_services.lobby_action import AsyncLobbyAction

from apps.chat.services.model_services import like_for_message, send_message, send_message_by_username
from apps.chat.cunsumers.base import ConsumerBase
from apps.chat.services.action_services.schemas import MessageLikeRequest, MessageSendResponce, MessageSendRequest
from apps.lobby.services.model_services import get_lobby
from apps.contact.services.model_services import get_contact_instance_by_his_id


class ChatConsumerLobby(ConsumerBase):
    available_receive_fields = (
        'type', 'text', 'voice_record', 'message_id',
        'status', 'reply_message', 'files'
    )
    
    async def preconnect(self) -> str:
        self.lobby_indentical: str = self.scope['url_route']['kwargs'].get('lobby_name', '')
        self.lobby = await sync_to_async(get_lobby)(lobby_name=self.lobby_indentical)
        self.action = AsyncLobbyAction(self.lobby)

        return f'lobby_{self.lobby_indentical.replace(" ", "_")}'
    
    async def receive_message(self, fields: dict[str, Any]) -> None:
        fields['user'] = self.user
        message_type = self.action.decode_json(fields, MessageSendRequest)
        message = await self.action.send_message(message_type)
        
        await self.sendint_to_group(group_name=self.group_name,
                                    event_method_name='chat_message',
                                    sending_data={
                                        **asdict(message),
                                    })

    async def receive_delete_like(self, fields: dict[str, Any]) -> None:
        await sync_to_async(like_for_message)(self.lobby, fields['message_id'], self.user.username, False)
        
        await self.sendint_to_group(group_name=self.group_name,
                                    event_method_name='chat_delete_like',
                                    sending_data={
                                        **fields,
                                    })
    
    async def receive_like(self, fields: dict[str, Any]) -> None:
        fields['user'] = self.user
        message_type = self.action.decode_json(fields, MessageLikeRequest)
        print(message_type)
        message = await self.action.like_message(message_type)
        
        await self.sendint_to_group(group_name=self.group_name,
                                    event_method_name='chat_like',
                                    sending_data={
                                        **asdict(message),
                                    })
    
    async def chat_like(self, event):
        await self.send(
            text_data=json.dumps({
                **event
            })
        )
        
    async def chat_delete_like(self, event):
        await self.chat_like(event)
    
    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps({
                **event
            })
        )


class ChatConsumerContact(ChatConsumerLobby):
    async def preconnect(self) -> str:
        self.contact_id: str = self.scope['url_route']['kwargs'].get('contact_id', '')
        self.lobby = await sync_to_async(get_contact_instance_by_his_id)(contact_id=int(self.contact_id))
        self.action = AsyncLobbyAction(self.lobby)
        
        return f'lobby_{self.contact_id.replace(" ", "_")}'