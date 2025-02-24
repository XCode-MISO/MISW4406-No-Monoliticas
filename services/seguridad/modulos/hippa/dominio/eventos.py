from __future__ import annotations
from dataclasses import dataclass, field
from seguridad.seedwork.dominio.eventos import (EventoDominio)
from seguridad.modulos.hippa.dominio.objetos_valor import (Status)
from datetime import datetime
import   uuid

@dataclass
class ValidacionHippaCreada(EventoDominio):
    id_anonimizacion: uuid.UUID = None
    fecha_creacion: datetime = None

@dataclass
class HippaAgregada(EventoDominio):
    id_reserva: uuid.UUID = None
    id_cliente: uuid.UUID = None
    estado: str = None
    fecha_creacion: datetime = None
    
@dataclass
class ValidacionHippaIniciada(EventoDominio):
    id_anonimizacion: uuid.UUID = None
    fecha_actualizacion: datetime = None

@dataclass
class ValidacionHippaCancelada(EventoDominio):
    id_anonimizacion: uuid.UUID = None
    fecha_actualizacion: datetime = None

@dataclass
class ValidacionHippaFinalizada(EventoDominio):
    id_anonimizacion: uuid.UUID = None
    fecha_finalizacion: datetime = None
    imagen: str = None
    estado: Status = None