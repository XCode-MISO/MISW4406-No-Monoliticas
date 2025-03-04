"""Entidades del dominio de vuelos

En este archivo usted encontrará las entidades del dominio de vuelos

"""

from __future__ import annotations
from dataclasses import dataclass, field
from autorizacion.modulos.envio_imagen.dominio.eventos import Envio_ImagenAgregada
import autorizacion.modulos.envio_imagen.dominio.objetos_valor as ov

from autorizacion.modulos.envio_imagen.dominio.objetos_valor import Status
from autorizacion.seedwork.dominio.entidades import AgregacionRaiz, Entidad
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
class ValidacionEnvio_Imagen(Entidad):
    id: str = field(default_factory=str)
    image: Imagen = field(default_factory=Imagen)
    estado: Status = field(default_factory=Status)

    def __str__(self) -> str:
        return self.id
    
    
@dataclass
class ValidacionesEnvio_Imagen(AgregacionRaiz):
    id: str = field(default_factory=str)
    image: Imagen = field(default_factory=Imagen)
    estado: Status = field(default_factory=Status)

    def crear_validaciones_envio_imagen(self, validaciones_envio_imagen: ValidacionesEnvio_Imagen):
        self.id = validaciones_envio_imagen.id
        self.imagen = validaciones_envio_imagen.imagen
        self.estado = validaciones_envio_imagen.estado
        self.agregar_evento(Envio_ImagenAgregada(id=self.id, fecha_validacion=self.fecha_validacion))
