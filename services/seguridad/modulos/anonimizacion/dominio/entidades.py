"""Entidades del dominio de vuelos

En este archivo usted encontrará las entidades del dominio de vuelos

"""

from __future__ import annotations
from dataclasses import dataclass, field

import seguridad.modulos.anonimizacion.dominio.objetos_valor as ov
from seguridad.modulos.anonimizacion.dominio.eventos import AnonimizacionAgregada
from seguridad.seedwork.dominio.entidades import AgregacionRaiz, Entidad

@dataclass
class Anonimizacion(AgregacionRaiz):
    nombre: str = field(default_factory=str)
    imagen: str = field(default_factory=str)
    fecha_fin: str = field(default_factory=str)

    def crear_anonimizacion(self, anonimizacion: Anonimizacion):
        self.nombre = anonimizacion.nombre
        self.imagen = anonimizacion.imagen
        self.fecha_fin = anonimizacion.fecha_fin
        self.agregar_evento(AnonimizacionAgregada(id_reserva=self.id, fecha_creacion=self.fecha_creacion))
