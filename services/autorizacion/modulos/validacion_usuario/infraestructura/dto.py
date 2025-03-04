from sqlalchemy.orm import declarative_base, relationship
from autorizacion.config.db import db
from sqlalchemy import Column, ForeignKey, Integer, Table

from datetime import datetime

import uuid

Base = db.declarative_base()

# class Validacion_Usuario(db.Model):
#     __tablename__ = "validacion_usuario"
#     id = db.Column(db.String, primary_key=True, default=str(uuid.uuid4()))
#     fecha_validacion = db.Column(db.DateTime, nullable=False)
#     fecha_actualizacion = db.Column(db.DateTime, nullable=False)
#     nombre = db.Column(db.String, nullable=False)
#     imagen = db.Column(db.String, nullable=False)
#     fecha_fin = db.Column(db.Integer, nullable=False)

class Validacion_Usuario(db.Model):
    __tablename__ = "validacion_usuario"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    fecha_actualizacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    fecha_validacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    usuario = db.Column(db.String(255), nullable=False)
    imagen = db.Column(db.String(255), nullable=False)

    
class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    usuario = db.Column(db.String(255), nullable=False)