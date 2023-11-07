from datetime import datetime

from pydantic import BaseModel


class ChatRoom(BaseModel):
    id: int
    title: str
    created_at: datetime

    class Config:
        orm_mode = True
