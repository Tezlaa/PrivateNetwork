from email import message
import os
import base64
from dataclasses import asdict
import time

from typing import Any, Optional, TypeVar

from asgiref.sync import sync_to_async

from django.core.files.base import ContentFile
from django.db import transaction
from django.db.models import FileField
from django.shortcuts import get_object_or_404
from apps.accounts.models import User

from apps.chat.models import Message, FileMessage
from apps.chat.services.action_services.schemas import (
    FileMessageType, FileUrl, MessageLikeRequest, MessageLikeResponse, MessageSendResponce, MessageSendRequest, ReplyMessage, UserAsUsername
)
from apps.contact.models import Contact
from apps.lobby.models import Lobby
from config.conf.media import MEDIA_URL


T = TypeVar('T')


class ActionBase:
    def decode_json(self, json: dict, schemas: T) -> T:
        reply_message = json.get('reply_message')
        files = json.get('files')
        voice_record = json.get('voice_record')
        
        if reply_message:
            json['reply_message'] = ReplyMessage(**reply_message)
        
        if (files and (isinstance(files, list)) and not
                (all(isinstance(file, FileMessageType) for file in files))):
            json['files'] = [self.decode_from_base64_utf8(file_dict) for file_dict in files]
        
        if voice_record and not isinstance(voice_record, FileMessageType):
            json['voice_record'] = self.decode_from_base64_utf8(voice_record)
        
        return schemas(**json)

    def decode_from_base64_utf8(self, file: dict) -> FileMessageType:
        file['file'] = base64.b64decode(file['file'].encode('utf-8'))
        return FileMessageType(**file)
    
    def encode_to_base64_utf8(self, file: FileMessage) -> dict[str, str]:
        json = asdict(file)
        json['file'] = base64.b64encode(file.file).decode('utf-8')
        
        return json

    def get_reply_message(self, reply: ReplyMessage) -> Optional[Message]:
        if reply is None:
            return
        
        return Message.objects.get(id=reply.id)
    
    def create_files(self, files: list[FileMessageType]) -> Optional[list[FileMessage]]:
        if files is None:
            return []
        
        return [self.get_file_instance(file) for file in files]

    def get_file_instance(self, file: FileMessage) -> Optional[FileMessage]:
        if file is None:
            return
        
        file_instance = FileMessage(sign=file.sign)
        file_instance.file.save(file.file_name, ContentFile(file.file))
        return file_instance
    
    def get_madia_path(self, message: FileField) -> str:
        return os.path.join(MEDIA_URL, str(message))
    
    def encode_json(self, event: MessageSendRequest) -> dict:
        result_json = asdict(event)
        files = result_json.get('files')
        voice_record = result_json.get('voice_record')
        
        if files:
            result_json['files'] = [self.encode_to_base64_utf8(file) for file in files]
        
        if voice_record:
            result_json['voice_record'] = self.encode_to_base64_utf8(voice_record)

    def asdict(schemas: T) -> dict:
        result_dict = asdict(schemas)
        
        user_instance = result_dict.get('user')
        if isinstance(user_instance, User):
            result_dict['user'] = asdict(UserAsUsername(username=user_instance.username, ))
        return result_dict
    

class LobbyAction(ActionBase):
    def __init__(self, lobby: Lobby | Contact) -> None:
        self.lobby = lobby

    @transaction.atomic
    def send_message(self, message: MessageSendRequest) -> MessageSendResponce:
        voice_answer = None
        files_answer = []
        reply_message_answer = None
        
        message_instance = Message.objects.create(
            user=message.user,
            message=message.text
        )
        
        voice = message.voice_record
        if voice is not None:
            message_instance.voice_record.save(voice.file_name, ContentFile(voice.file))
            voice_answer = FileUrl(url=self.get_madia_path(message_instance.voice_record))
        
        for file in self.create_files(message.files):
            message_instance.files.add(file)
            files_answer.append(FileUrl(url=self.get_madia_path(file.file)))
        
        message_instance.reply_message = self.get_reply_message(message.reply_message)
        if message_instance.reply_message:
            reply_message_answer = ReplyMessage(id=message_instance.reply_message.id)
        
        self.lobby.chat.add(
            message_instance
        )
        self.lobby.save()
        
        return MessageSendResponce(
            user=UserAsUsername(username=message.user.username),
            text=message.text,
            message_id=message_instance.id,
            voice_record=voice_answer,
            reply_message=reply_message_answer,
            timestamp=int(round(message_instance.created_at.timestamp())),
            files=files_answer
        )
    
    @transaction.atomic
    def like_message(self, message: MessageLikeRequest) -> MessageLikeResponse:
        message_instance = get_object_or_404(Message, id=message.message_id)
        user_like = message_instance.user_liked
        
        if user_like.exists() and not message.status:
            user_like.remove(message.user)
        elif not user_like.exists() and message.status:
            user_like.add(message.user)
        
        message_instance.save()

        return MessageLikeResponse(
            user=UserAsUsername(username=message.user.username),
            message_id=message.message_id,
            status=message.status
        )
    

class AsyncLobbyAction(LobbyAction):
    
    @sync_to_async
    def send_message(self, message: MessageSendRequest) -> MessageSendResponce:
        return super().send_message(message)
    
    @sync_to_async
    def like_message(self, message: MessageLikeRequest) -> MessageLikeResponse:
        return super().like_message(message)