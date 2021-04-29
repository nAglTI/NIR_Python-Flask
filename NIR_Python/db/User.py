from sqlalchemy import Column, VARCHAR, Integer

from db.Base import Base


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, index=True, unique=True, primary_key=True, autoincrement=True)

    login = Column(VARCHAR(16), index=True, unique=True)

    password = Column(VARCHAR(20))
