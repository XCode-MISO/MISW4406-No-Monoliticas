
from ingestion_datos.config.db import Base
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table, Date, String

import uuid

class OrquestracionLog(Base):
    __tablename__ = "orquestracion_log"
    fecha = Column(Date, primary_key=True)
    nombre = Column(Integer, primary_key=True, nullable=False)
    id_evento = Column(String, primary_key=True, nullable=False)