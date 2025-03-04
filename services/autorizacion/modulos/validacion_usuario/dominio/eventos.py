from __future__ import annotations
from dataclasses import dataclass, field
from autorizacion.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime
import uuid

@dataclass
class Validacion_UsuarioCreada(EventoDominio):
    id_validacion_usuario: uuid.UUID = None
    imagen: str = None
    fecha_validacion: datetime = None
    
@dataclass
class Validacion_UsuarioAgregada(EventoDominio):
    id_reserva: uuid.UUID = None
    id_cliente: uuid.UUID = None
    estado: str = None
    fecha_validacion: datetime = None
    
    
@dataclass
class Validacion_UsuarioIniciada(EventoDominio):
    id_validacion_usuario: uuid.UUID = None
    fecha_actualizacion: datetime = None

@dataclass
class Validacion_UsuarioCancelada(EventoDominio):
    id_validacion_usuario: uuid.UUID = None
    fecha_actualizacion: datetime = None

@dataclass
class Validacion_UsuarioFinalizada(EventoDominio):
     id: str = None
     id_correlacion: str = None
     ingestion_id: str = None
     imagen: str = None
     nombre: str = None
     fecha_creacion: str = None
    
#####################################****************************************############################################
@dataclass
class UsuarioCreada(EventoDominio):
    id_usuario: uuid.UUID = None
    usuario: str = None
    
@dataclass
class UsuarioAgregada(EventoDominio):
    id_reserva: uuid.UUID = None
    usuario: str = None
    
    
@dataclass
class UsuarioIniciada(EventoDominio):
    id_usuario: uuid.UUID = None
    fecha_actualizacion: datetime = None

@dataclass
class UsuarioCancelada(EventoDominio):
    id_vusuario: uuid.UUID = None
    fecha_actualizacion: datetime = None

@dataclass
class UsuarioFinalizada(EventoDominio):
    id_usuario: uuid.UUID = None