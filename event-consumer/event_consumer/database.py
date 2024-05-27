import sqlalchemy as db

from sqlalchemy.orm import sessionmaker
from .settings import DatabaseSettings
from .models import Base, Event


class DatabaseConnection:
    def __init__(self) -> None:
        self.settings = DatabaseSettings()
        self.db_engine = self.create_connection()
        self.metadata = Base.metadata
        self.Session = sessionmaker(bind=self.db_engine)
        self.create_events_table()

    def create_connection(self) -> object:
        db_engine = db.create_engine(
            f"mysql+mysqlconnector://"
            f"{self.settings.mysql_user}:{self.settings.mysql_password}"
            f"@{self.settings.mysql_host}:{int(self.settings.mysql_port)}"
            f"/{self.settings.mysql_database}"
        )
        return db_engine

    def create_events_table(self):
        self.metadata.create_all(self.db_engine)

    def get_all_events(self):
        session = self.Session()
        try:
            events = session.query(Event).all()
            return events
        finally:
            session.close()

    def post_event(self, type, payload):
        Session = sessionmaker(bind=self.db_engine)
        session = Session()

        try:
            new_event = Event(type=type, payload=payload)
            session.add(new_event)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
