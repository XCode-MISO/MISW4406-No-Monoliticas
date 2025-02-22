"""Entidades del dominio de vuelos

En este archivo usted encontrará las entidades del dominio de vuelos

"""

from __future__ import annotations
from dataclasses import dataclass, field

import pda.modulos.anonimizacion.dominio.objetos_valor as ov
from pda.modulos.anonimización.dominio.eventos import ReservaCreada, ReservaAprobada, ReservaCancelada, ReservaPagada
from pda.seedwork.dominio.entidades import Entidad

@dataclass
class Anonimizacion(Entidad):
    fecha_fin: datetime = field(default=None)
    image: string = field(default_factory=str)

    def __str__(self) -> str:
        return self.id
