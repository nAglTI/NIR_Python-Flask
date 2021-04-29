from sqlalchemy import Column, VARCHAR, Integer, Text, ForeignKey

from db.Base import Base


class Message(Base):
    __tablename__ = "message"

    mess_id = Column(Integer, index=True, unique=True, primary_key=True, autoincrement=True)

    text = Column(Text)

    user_id = Column(Integer, ForeignKey("user.user_id"))
