from typing import Optional

from django.core.files import File
from django.db import transaction

from apps.chat.models import Message, FileMessage
from apps.chat.services.schemas import FileMessageType, MessageSendType, ReplyMessage
from apps.contact.models import Contact
from apps.lobby.models import Lobby


class LobbyAction:
    def __init__(self, lobby: Lobby | Contact) -> None:
        self.lobby = lobby

    @transaction.atomic
    def send_message(self, message: MessageSendType) -> Message: 
        message_instance = Message.objects.create(
            user=message.user,
            message=message.text
        )
        
        message_instance.voice_record = self.get_file(message.voice_record)
        
        for file in self.create_files(message.files):
            message_instance.files.add(file)
        
        message_instance.reply_message = self.get_reply_message(message.reply_message)
        
        self.lobby.chat.add(
            message_instance
        )
        self.lobby.save()
        
        return message_instance

    def get_reply_message(self, reply: ReplyMessage) -> Optional[Message]:
        if reply is None:
            return
        
        return Message.objects.get(id=reply.id)
        
    def create_files(self, files: list[FileMessageType]) -> Optional[list[FileMessage]]:
        if files is None:
            return
        
        return FileMessage.objects.bulk_create([
            FileMessage(
                sign=file.sign,
                file=self.get_file(file)
            ) for file in files
        ])

    def get_file(self, file: FileMessage) -> Optional[File]:
        if file is None:
            return
        
        return File(file.file, name=file.file_name)

    
class AsyncMessage(Message):
    async def send_message(message: MessageSendType):
        pass