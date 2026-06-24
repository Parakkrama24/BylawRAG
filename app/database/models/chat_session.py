from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from datetime import datetime

from app.database.models import Base


class ChatSession(Base):

    __tablename__ = "chat_sessions"

    id = Column(
        String,
        primary_key=True,
        index=True
    )

    title = Column(
        String
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )