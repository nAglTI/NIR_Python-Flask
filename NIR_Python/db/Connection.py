import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from db.Base import Base
from db.Message import Message
from db.User import User


class Connection:
    def __init__(self):
        self.User = User
        self.Message = Message

        with open("res/db.json") as secret_file:
            secret = json.load(secret_file)

        engine = create_engine(secret["db-url"], echo=True)

        for table in (User, Message):
            if not engine.dialect.has_table(engine.connect(), table.__name__):
                Base.metadata.create_all(engine)

                break

        self.__session = sessionmaker()
        self.__session.configure(bind=engine)

    def session(self) -> Session:
        return self.__session()
