from seguridad.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table

import uuid

Base = db.declarative_base()

class Anonimizacion(db.Model):
    __tablename__ = "anonimizacion"
    id = db.Column(db.String, primary_key=True, default=str(uuid.uuid4()))
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False)
    nombre = db.Column(db.String, nullable=False)
    imagen = db.Column(db.String, nullable=False)
    fecha_fin = db.Column(db.Integer, nullable=False)