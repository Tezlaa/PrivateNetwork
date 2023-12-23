from typing import Any, Coroutine
from apps.chat.cunsumers.chat_consumer import ChatConsumer


class NotifyConsumer(ChatConsumer):
    
    async def preconnect(self) -> str:
        self.lobbies = self.scope['headers']
        return ''
    
    async def connect(self):
        await self.preconnect()
        
        for lobby in self.lobbies:
            await self.channel_layer.group_add(f'lobby_{lobby}', self.channel_name)  # type: ignore
        
        await self.accept()