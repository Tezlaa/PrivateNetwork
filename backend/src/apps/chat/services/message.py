import io

from typing import Optional

from django.core.files.base import ContentFile
from django.db import transaction
from django.db.models import FileField

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
        
        voice = message.voice_record
        if voice is not None:
            message_instance.voice_record.save(voice.file_name, ContentFile(voice.file))
        
        for file in self.create_files(message.files):
            message_instance.files.add(file)
        
        message_instance.reply_message = self.get_reply_message(message.reply_message)
        
        self.lobby.chat.add(
            message_instance
        )
        self.lobby.save()
        
        return message_instance

    def typed_json(self, json: dict) -> MessageSendType:
        reply_message = json.get('reply_message')
        files = json.get('files')
        voice_record = json.get('voice_record')
        
        if reply_message:
            json['reply_message'] = ReplyMessage(**reply_message)
        
        if (files and (isinstance(files, list)) and not
                (all(isinstance(file, FileMessageType) for file in files))):
            json['files'] = [FileMessageType(**file_dict) for file_dict in files]
        
        if voice_record and not isinstance(voice_record, FileMessageType):
            json['voice_record'] = FileMessageType(**voice_record)
        return MessageSendType(**json)

    def get_reply_message(self, reply: ReplyMessage) -> Optional[Message]:
        if reply is None:
            return
        
        return Message.objects.get(id=reply.id)
    
    def create_files(self, files: list[FileMessageType]) -> Optional[list[FileMessage]]:
        if files is None:
            return
        
        return [self.get_file_instance(file) for file in files]

    def get_file_instance(self, file: FileMessage) -> Optional[FileMessage]:
        if file is None:
            return
        
        file_instance = FileMessage(sign=file.sign)
        file_instance.file.save(file.file_name, ContentFile(file.file))
        return file_instance
    
    def get_madia_path(self, message: FileField):
        return str(message.file).split('\\media\\')[1].replace('\\', '/')