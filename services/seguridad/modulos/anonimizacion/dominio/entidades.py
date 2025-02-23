"""Entidades del dominio de vuelos

En este archivo usted encontrará las entidades del dominio de vuelos

"""

from __future__ import annotations
from dataclasses import dataclass, field

import seguridad.modulos.anonimizacion.dominio.objetos_valor as ov
from seguridad.seedwork.dominio.entidades import Entidad

@dataclass
class Anonimizacion(Entidad):
    fecha_fin: datetime = field(default=None)
    image: string = field(default_factory=str)

    def __str__(self) -> str:
        return self.id
