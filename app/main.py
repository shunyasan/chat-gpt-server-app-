import uvicorn
from starlette.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .schemas.chatMessage import ChatMessage, PostChatMessage
from .schemas.chatRoom import ChatRoom

from .services import chatMessageService, chatRoomService

from . import models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/chat-room/", response_model=list[ChatRoom])
def get_chat_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return chatRoomService.get_chat_rooms(db, skip=skip, limit=limit)


@app.get("/chat-room/{chat_room_id}", response_model=ChatRoom)
def get_chat_room(chat_room_id:int, db: Session = Depends(get_db)):
    return chatRoomService.get_chat_room(db, chat_room_id)


@app.get("/chat-room/{chat_room_id}/chat-message", response_model=list[ChatMessage])
def get_chat_messages(chat_room_id:int,skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return chatMessageService.get_chat_messages(db, chat_room_id, skip=skip, limit=limit)


@app.post("/chat-room/first/chat-message", ) #response_model=schemasChatMessage
def post_chat_message(post_chat_message: PostChatMessage, db: Session = Depends(get_db)):
    return chatMessageService.first_post_chat_message(db, content=post_chat_message.content)


@app.post("/chat-room/{chat_room_id}/chat-message") #response_model=schemasChatMessage
def post_chat_message(chat_room_id:int, post_chat_message: PostChatMessage, db: Session = Depends(get_db)):
    return chatMessageService.continue_post_chat_message(db,  chat_room_id=chat_room_id, content=post_chat_message.content)


#########################
# Server Setting
#########################

# 許容するオリジン (CORS設定)
origins = [
  "http://localhost:3000",
  "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
)
# 起動
if __name__ == "__main__":
    uvicorn.run(app,)
