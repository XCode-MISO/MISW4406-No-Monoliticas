from pulsar.schema import *
from dataclasses import dataclass, field
from autorizacion.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)
from autorizacion.seedwork.aplicacion.comandos import Comando

class ComandoCrearValidacion_UsuarioPayload(ComandoIntegracion):
    fecha_actualizacion = String()
    fecha_validacion  = String()
    id = String()
    usuario = String()
    nombre = String()
    imagen = String()
    fecha_fin = String()

class ComandoCrearValidacion_Usuario(ComandoIntegracion):
    data = ComandoCrearValidacion_UsuarioPayload()
@dataclass
class CrearValidacion_Usuario(Comando):
    fecha_validacion: str
    fecha_actualizacion: str
    id: str
    usuario: str
    nombre: str
    imagen: str
    fecha_fin: str

################################################################
class ComandoErrorValidacion_UsuarioPayload(ComandoIntegracion):
    nombre = String()

class ComandoErrorValidacion_Usuario(ComandoIntegracion):
    data = ComandoErrorValidacion_UsuarioPayload()
    
@dataclass
class ErrorValidacion_Usuario(Comando):
    nombre: str
################################################################