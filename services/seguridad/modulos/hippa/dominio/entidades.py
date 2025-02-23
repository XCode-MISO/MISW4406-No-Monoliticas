"""Entidades del dominio de vuelos

En este archivo usted encontrará las entidades del dominio de vuelos

"""

from __future__ import annotations
from dataclasses import dataclass, field

import seguridad.modulos.hippa.dominio.objetos_valor as ov
from seguridad.modulos.hippa.dominio.eventos import ReservaCreada, ReservaAprobada, ReservaCancelada, ReservaPagada
from seguridad.seedwork.dominio.entidades import Entidad
from seguridad.modulos.hippa.dominio.objetos_valor import Status

@dataclass
class ValidacionHippa(Entidad):
    fecha_fin: datetime = field(default=None)
    image: Imagen = field(default_factory=Imagen)
    razones: list[str] = field(default_factory=list[str])
    estado: Status = field(default_factory=Status)

    def __str__(self) -> str:
        return self.id

@dataclass
class Imagen(Entidad):
    image: str = field(default_factory=str)
    def tiene_informacion_personal() -> bool:
        return false
    def tiene_informacion_sanitaria() -> bool:
        return false
    def tiene_informacion_fisica() -> bool:
        return false
    def tiene_informacion_mental() -> bool:
        return false
    def tiene_informacion_de_pago() -> bool:
        return false
    def tiene_informacion_del_proveedor_sanitario() -> bool:
        return false