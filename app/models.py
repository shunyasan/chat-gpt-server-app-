import enum
from datetime import datetime

from sqlalchemy import Enum, Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship

from .database import Base


class ChatRoom(Base):
    __tablename__ = "chat_room"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(40), nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)

    chat_messages = relationship("ChatMessage", back_populates="chat_room")


class RoleType(str, enum.Enum):
    system = "system" # 最初の会話
    user = "user" # 質問者
    assistant = "assistant" # ChatGPTの回答


class ChatMessage(Base):
    __tablename__ ="chat_message"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(Enum(RoleType),nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    chat_room_id = Column(Integer, ForeignKey("chat_room.id"), nullable=False)

    chat_room = relationship("ChatRoom", back_populates="chat_messages")

