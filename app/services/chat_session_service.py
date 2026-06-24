import uuid

from sqlalchemy import func

from app.database.models import SessionLocal
from app.database.models.chat_message import ChatMessage
from app.database.models.chat_session import ChatSession


def create_session():

    db = SessionLocal()

    session_id = str(uuid.uuid4())

    session = ChatSession(
        id=session_id,
        title="New Chat"
    )

    db.add(session)

    db.commit()

    db.close()

    return session_id


def update_session_title(
        session_id,
        question):

    db = SessionLocal()

    session = (
        db.query(ChatSession)
        .filter(
            ChatSession.id == session_id
        )
        .first()
    )

    if session.title == "New Chat":

        session.title = question[:40]

        db.commit()

    db.close()

def get_sessions():

    db = SessionLocal()

    sessions = (
        db.query(
            ChatSession,
            func.count(ChatMessage.id)
        )
        .outerjoin(
            ChatMessage,
            ChatSession.id == ChatMessage.session_id
        )
        .group_by(
            ChatSession.id
        )
        .all()
    )

    db.close()

    result = []

    for session, count in sessions:

        result.append({
            "id": session.id,
            "title": session.title,
            "message_count": count,
            "created_at": session.created_at
        })

    return result

def get_session_messages(session_id):

    db = SessionLocal()

    messages = (
        db.query(ChatMessage)
        .filter(
            ChatMessage.session_id == session_id
        )
        .order_by(
            ChatMessage.created_at.asc()
        )
        .all()
    )

    db.close()

    return messages

def delete_session(session_id):

    db = SessionLocal()

    session = (
        db.query(ChatSession)
        .filter(
            ChatSession.id == session_id
        )
        .first()
    )

    if not session:
        db.close()

        return {
            "message": "Session not found"
        }

    db.delete(session)

    db.query(ChatSession).filter(
        ChatSession.id == session_id
    ).delete()

    db.commit()

    db.close()

    return {
        "message": "Session deleted"
    }