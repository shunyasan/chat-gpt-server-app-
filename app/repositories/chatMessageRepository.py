from sqlalchemy.orm import Session

from .. import models


def get_chat_messages(db: Session,chat_room_id:int, skip: int = 0, limit: int = 100):
    return db.query(models.ChatMessage).filter(models.ChatMessage.chat_room_id == chat_room_id).order_by(models.ChatMessage.created_at).offset(skip).limit(limit).all()

