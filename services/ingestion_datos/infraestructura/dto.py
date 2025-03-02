
from ingestion_datos.config.db import Base
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table, Date

import uuid

class IngestionDatosAnalitica(Base):
    __tablename__ = "analitica_ingestion_datos"
    fecha_creacion = Column(Date, primary_key=True)
    total = Column(Integer, primary_key=True, nullable=False)