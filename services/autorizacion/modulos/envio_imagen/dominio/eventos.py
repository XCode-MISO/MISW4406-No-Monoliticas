from __future__ import annotations
from dataclasses import dataclass, field
from autorizacion.seedwork.dominio.eventos import (EventoDominio)
from autorizacion.modulos.envio_imagen.dominio.objetos_valor import (Status)
from datetime import datetime
import   uuid

@dataclass
class ValidacionEnvio_ImagenCreada(EventoDominio):
    id: uuid.UUID = None
    fecha_validacion: datetime = None

@dataclass
class Envio_ImagenAgregada(EventoDominio):
    id: uuid.UUID = None
    estado: str = None
    fecha_validacion: datetime = None
    
@dataclass
class ValidacionEnvio_ImagenIniciada(EventoDominio):
    id: uuid.UUID = None
    fecha_actualizacion: datetime = None

@dataclass
class ValidacionEnvio_ImagenCancelada(EventoDominio):
    id: uuid.UUID = None
    fecha_actualizacion: datetime = None

@dataclass
class ValidacionEnvio_ImagenFinalizada(EventoDominio):
    id: uuid.UUID = None
    fecha_finalizacion: datetime = None
    imagen: str = None
    estado: Status = None