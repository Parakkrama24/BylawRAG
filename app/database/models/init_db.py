from app.database.models import Base, engine
from app.database.models.chat_message import ChatMessage


def create_tables():

    Base.metadata.create_all(
        bind=engine
    )