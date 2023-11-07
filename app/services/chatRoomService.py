from sqlalchemy.orm import Session

from ..repositories import chatRoomRepository


def get_chat_rooms(db: Session, skip: int = 0, limit: int = 100):
    return chatRoomRepository.get_chat_rooms(db, skip=skip, limit=limit)


def get_chat_room(db: Session, chat_room_id: int):
    return chatRoomRepository.get_chat_room(db, chat_room_id)

