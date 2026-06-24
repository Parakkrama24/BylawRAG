from app.database.models import SessionLocal
from app.database.models.chat_message import ChatMessage


def get_chat_history(session_id):

    db = SessionLocal()

    messages = (
        db.query(ChatMessage)
        .filter(
            ChatMessage.session_id == session_id
        )
        .order_by(
            ChatMessage.created_at
        )
        .all()
    )

    db.close()

    return [
        {
            "role": msg.role,
            "content": msg.content
        }
        for msg in messages
    ]


def add_message(
        session_id,
        role,
        content):

    db = SessionLocal()

    message = ChatMessage(
        session_id=session_id,
        role=role,
        content=content
    )

    db.add(message)

    db.commit()

    db.close()