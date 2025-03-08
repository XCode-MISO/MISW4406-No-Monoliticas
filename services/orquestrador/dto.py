
import datetime
from orquestrador.config.db import Base
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table, Date, String, TIMESTAMP, func

import uuid

class OrquestracionLog(Base):
    __tablename__ = "orquestracion_log"
    nombre = Column(String(200), primary_key=True, nullable=False)
    id_evento = Column(String(200), primary_key=True, nullable=False)
    fecha = Column(Date, primary_key=True)
    timestamp = Column(TIMESTAMP, primary_key=True, server_default=func.current_timestamp())