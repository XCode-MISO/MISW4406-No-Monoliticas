from __future__ import annotations
from dataclasses import dataclass, field
from pda.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime

@dataclass
class AnonimizacionCreada(EventoDominio):
    id_anonimizacion: uuid.UUID = None
    imagen: str = None
    fecha_creacion: datetime = None
    

@dataclass
class AnonimizacionIniciada(EventoDominio):
    id_anonimizacion: uuid.UUID = None
    fecha_actualizacion: datetime = None

@dataclass
class AnonimizacionCancelada(EventoDominio):
    id_anonimizacion: uuid.UUID = None
    fecha_actualizacion: datetime = None

@dataclass
class AnonimizacionFinalizada(EventoDominio):
    id_anonimizacion: uuid.UUID = None
    fecha_actualizacion: datetime = None
    fecha_finalizacion: datetime = None
    imagen: str = None