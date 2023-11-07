from datetime import datetime
from sqlalchemy.orm import Session

from .. import models


def get_chat_rooms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ChatRoom).offset(skip).limit(limit).all()


def get_chat_room(db: Session, chat_room_id: int):
    return db.query(models.ChatRoom).filter(models.ChatRoom.id == chat_room_id).first()


def create_chat_room_no_commit(db: Session, title: str):
    new_chat_room = models.ChatRoom(
        title=title,
        created_at = datetime.now(),
    )
    db.add(new_chat_room)
    db.flush()
    db.refresh(new_chat_room)
    return new_chat_room
