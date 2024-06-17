from sqlalchemy import Column, Integer, String, DateTime, JSON
from db import Base, engine
from datetime import datetime


class Mensajes(Base):
    __tablename__ = "mensajes"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    subject = Column(String(50), unique=False, index=True)
    message = Column(String(50), unique=False, index=True)
    person = Column(JSON)
    contact = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)


Base.metadata.create_all(bind=engine)


