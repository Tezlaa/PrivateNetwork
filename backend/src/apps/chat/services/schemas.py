from dataclasses import dataclass

from typing import Optional

from apps.accounts.models import User


@dataclass
class ReplyMessage:
    id: int


@dataclass
class FileMessageType:
    file: bytes
    file_name: str
    sign: Optional[str] = None


@dataclass
class MessageSendType:
    user: User
    text: Optional[str] = None
    voice_record: Optional[FileMessageType] = None
    reply_message: Optional[ReplyMessage] = None
    files: Optional[list[FileMessageType]] = None


@dataclass
class MessageReceiveType(MessageSendType):
    timestamp: Optional[str] = None