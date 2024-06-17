from sqlalchemy import Column, Integer, String, JSON, DateTime
from db import Base, engine
from datetime import datetime


class Cotizacion(Base):
    __tablename__ = "cotizaciones"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    type = Column(String(50), unique=False, index=True)
    objeto_cotizado = Column(JSON)
    info_add = Column(JSON)
    person = Column(JSON)
    contact = Column(JSON)
    address = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)


Base.metadata.create_all(bind=engine)
