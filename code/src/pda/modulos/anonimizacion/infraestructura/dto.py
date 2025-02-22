"""DTOs para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de vuelos

"""

from pda.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table

import uuid

Base = db.declarative_base()

# Tabla intermedia para tener la relación de muchos a muchos entre la tabla anonimizacion e itinerarios
anonimizaciones = db.Table(
    "anonimizaciones",
    db.Model.metadata,
    db.Column("anonimizacion_id", db.String,
              db.ForeignKey("anonimizacion.id")),
    db.Column("odo_orden", db.Integer),
    db.Column("segmento_orden", db.Integer),
    db.Column("leg_orden", db.Integer),
    db.Column("fecha_salida", db.DateTime),
    db.Column("fecha_llegada", db.DateTime),
    db.Column("origen_codigo", db.String),
    db.Column("destino_codigo", db.String),
)


class Anonimzacion(db.Model):
    __tablename__ = "anonimizacion"
    id = db.Column(db.String, primary_key=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)
    imagen = db.Column(db.String, nullable=False)
