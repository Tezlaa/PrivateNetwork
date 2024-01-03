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
class FileUrl:
    url: str


@dataclass
class UserAsUsername:
    username: str


@dataclass
class MessageSendRequest:
    user: User
    text: Optional[str] = None
    voice_record: Optional[FileMessageType] = None
    reply_message: Optional[ReplyMessage] = None
    files: Optional[list[FileMessageType]] = None


@dataclass
class MessageSendResponce:
    user: UserAsUsername
    message_id: int
    text: Optional[str] = None
    voice_record: Optional[FileUrl] = None
    reply_message: Optional[ReplyMessage] = None
    files: Optional[list[FileUrl]] = None
    timestamp: Optional[str] = None
    

@dataclass
class MessageLikeRequest:
    user: User
    message_id: int
    status: bool = False


class MessageLikeResponse(MessageLikeRequest):
    user: UserAsUsername