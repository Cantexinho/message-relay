from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(255), nullable=False)
    payload = Column(Text)
    received_time = Column(
        TIMESTAMP, nullable=False, default=func.current_timestamp()
    )
