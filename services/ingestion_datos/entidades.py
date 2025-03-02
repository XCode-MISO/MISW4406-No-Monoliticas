"""Entidades del dominio de vuelos

En este archivo usted encontrará las entidades del dominio de vuelos

"""

from __future__ import annotations
from dataclasses import dataclass, field

from ingestion_datos.dominio.eventos import IngestionFinalizada
from seguridad.seedwork.dominio.entidades import Entidad

@dataclass
class IngestionDatos(Entidad):
    nombre: str = field(default_factory=str)
    imagen: str = field(default_factory=str)

    def crear_ingestion_datos(self, ingestion: IngestionDatos):
        self.nombre = ingestion.nombre
        self.imagen = ingestion.imagen
        self.agregar_evento(
            IngestionFinalizada(
            id=self.id, 
            fecha_creacion=self.fecha_creacion, 
            imagen=self.imagen
          ))
