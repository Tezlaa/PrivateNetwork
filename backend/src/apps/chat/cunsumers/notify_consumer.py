
from apps.chat.cunsumers.chat_consumer import ChatConsumerLobby


class NotifyConsumer(ChatConsumerLobby):
    
    async def preconnect(self) -> str:
        self.lobbies = self.scope['headers']
        self.group_names = []
        return ''
    
    async def connect(self):
        await self.preconnect()
        
        for lobby in self.lobbies:
            self.group_names.append(f'lobby_{lobby}')
            await self.channel_layer.group_add(f'lobby_{lobby}', self.channel_name)  # type: ignore

        await self.accept()
    
    async def disconnect(self, close_code):
        for group_name in self.group_names:
            await self.channel_layer.group_discard(group_name, self.channel_name)  # type: ignore