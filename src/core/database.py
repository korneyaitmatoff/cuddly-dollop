from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


class DatabaseEngine:
    DATABASE_CONNECTION_STRING: str
    session: Session | None

    def __init__(self, database_connection_string: str):
        self.DATABASE_CONNECTION_STRING = database_connection_string

        self.engine = create_engine(url=self.DATABASE_CONNECTION_STRING)
        self.session_maker = sessionmaker(bind=self.engine, expire_on_commit=True)
