import enum
from datetime import datetime

from pydantic import BaseModel


class ChatRoom(BaseModel):
    id: int
    title: str
    created_at: datetime

    class Config:
        orm_mode = True


class RoleType(str, enum.Enum):
    system = "system" # 最初の会話
    user = "user" # 質問者
    assistant = "assistant" # ChatGPTの回答


class PostChatMessage(BaseModel):
    content: str


class ChatMessage(BaseModel):
    id: int
    role: RoleType
    content: str
    created_at: datetime
    chat_room_id: int

    class Config:
        orm_mode = True


class GetChatGpt(BaseModel):
    role: RoleType
    content: str

