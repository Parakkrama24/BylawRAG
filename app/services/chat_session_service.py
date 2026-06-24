import uuid

from app.database.models import SessionLocal
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
        db.query(ChatSession)
        .order_by(
            ChatSession.created_at.desc()
        )
        .all()
    )

    db.close()

    return sessions