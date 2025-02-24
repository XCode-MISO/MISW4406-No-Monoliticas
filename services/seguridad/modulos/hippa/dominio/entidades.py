"""Entidades del dominio de vuelos

En este archivo usted encontrará las entidades del dominio de vuelos

"""

from __future__ import annotations
from dataclasses import dataclass, field
from seguridad.modulos.hippa.dominio.eventos import HippaAgregada
import seguridad.modulos.hippa.dominio.objetos_valor as ov

from seguridad.modulos.hippa.dominio.objetos_valor import Status
from seguridad.seedwork.dominio.entidades import AgregacionRaiz, Entidad
@dataclass
class Imagen(Entidad):
    image: str = field(default_factory=str)
    def tiene_informacion_personal() -> bool:
        return False
    def tiene_informacion_sanitaria() -> bool:
        return False
    def tiene_informacion_fisica() -> bool:
        return False
    def tiene_informacion_mental() -> bool:
        return False
    def tiene_informacion_de_pago() -> bool:
        return False
    def tiene_informacion_del_proveedor_sanitario() -> bool:
        return False

@dataclass
class ValidacionHippa(Entidad):
    id: str = field(default_factory=str)
    image: Imagen = field(default_factory=Imagen)
    estado: Status = field(default_factory=Status)

    def __str__(self) -> str:
        return self.id
    
    
@dataclass
class ValidacionesHippa(AgregacionRaiz):
    id: str = field(default_factory=str)
    image: Imagen = field(default_factory=Imagen)
    estado: Status = field(default_factory=Status)

    def crear_validaciones_hippa(self, validaciones_hippa: ValidacionesHippa):
        self.id = validaciones_hippa.id
        self.imagen = validaciones_hippa.imagen
        self.estado = validaciones_hippa.estado
        self.agregar_evento(HippaAgregada(id=self.id, fecha_creacion=self.fecha_creacion))
