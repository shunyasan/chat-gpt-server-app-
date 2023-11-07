from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from ..repositories import chatMessageRepository, chatRoomRepository
from .. import models

from . import chatGptService


def get_chat_messages(db: Session,chat_room_id:int, skip: int = 0, limit: int = 100):
    return chatMessageRepository.get_chat_messages(db, chat_room_id, skip=skip, limit=limit)


# 新規のChatRoomで質問をする
def first_post_chat_message(db: Session,content:str):
    # 質問を準備
    first_content = "聞きたいことは何ですか？"
    all_messages = [
        {"role": "system", "content": first_content},
        {"role": "user", "content": content}
    ]
    # chatGPTへ質問
    response_content = chatGptService.get_chat_gpt(all_messages)

    # ChatRoomとChatMessageを更新するのでTransaction
    try:
        # 初回はChatRoomも作成
        new_chat_room = chatRoomRepository.create_chat_room_no_commit(db,content[:20]+"...")

        # 初回の定型分
        first_message = models.ChatMessage(
            role=models.RoleType.system,
            content=first_content,
            created_at=datetime.now(),
            chat_room_id=new_chat_room.id
        )
        # 質問内容
        new_message = models.ChatMessage(
            role=models.RoleType.user,
            content=content,
            created_at=datetime.now() + timedelta(seconds=3),
            chat_room_id=new_chat_room.id
        )
        # chatGPTの回答
        new_message_response = models.ChatMessage(
            role=models.RoleType.assistant,
            content=response_content,
            created_at=datetime.now() + timedelta(seconds=6),
            chat_room_id=new_chat_room.id
        )
        # ChatMessageを追加して一括登録
        db.bulk_save_objects([first_message,new_message,new_message_response])
        db.commit()

        return new_message_response
    
    except:
        # 失敗した場合はロールバック
        db.rollback()
        raise Exception("トランザクションエラー")


# 既存のChatRoomで質問する
def continue_post_chat_message(db: Session,chat_room_id:int, content: str):
    # 過去の質問を追加して準備
    messages = chatMessageRepository.get_chat_messages(db,chat_room_id)
    message_history = [{"role": message.role, "content": message.content} for message in messages]
    all_messages =  message_history + [{"role": "user", "content": content}]
    # chatGPTへ質問
    response_content = chatGptService.get_chat_gpt(all_messages)

    # 質問内容
    new_message = models.ChatMessage(
        role=models.RoleType.user,
        content=content,
        created_at=datetime.now(),
        chat_room_id=chat_room_id
    )
    # chatGPTの回答
    new_message_response = models.ChatMessage(
        role=models.RoleType.assistant,
        content=response_content,
        created_at=datetime.now() + timedelta(seconds=3),
        chat_room_id=chat_room_id
    )
    # 一括登録
    db.bulk_save_objects([new_message,new_message_response])
    db.commit()

    return new_message_response

