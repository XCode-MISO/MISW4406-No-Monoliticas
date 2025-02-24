"""DTOs para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de vuelos

"""

from seguridad.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table

import uuid

Base = db.declarative_base()

class ValidacionHippa(db.Model):
    __tablename__ = "validacion_hippa"
    id = db.Column(db.String, primary_key=True, default=str(uuid.uuid4()))
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False)
    imagen = db.Column(db.String, nullable=False)
    estado = db.Column(db.String, nullable=False)
