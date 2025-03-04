"""DTOs para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de vuelos

"""

from autorizacion.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table

import uuid

from datetime import datetime

Base = db.declarative_base()

# class ValidacionEnvio_Imagen(db.Model):
#     __tablename__ = "validacion_envio_imagen"
#     id = db.Column(db.String, primary_key=True, default=str(uuid.uuid4()))
#     fecha_validacion = db.Column(db.DateTime, nullable=False)
#     fecha_actualizacion = db.Column(db.DateTime, nullable=False)
#     imagen = db.Column(db.String, nullable=False)
#     estado = db.Column(db.String, nullable=False)

class ValidacionEnvio_Imagen(db.Model):
    __tablename__ = "validacion_envio_imagen"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    fecha_validacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, server_default=db.text("CURRENT_TIMESTAMP"))
    fecha_actualizacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow, server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    imagen = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.String(50), nullable=False)