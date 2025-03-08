from pulsar.schema import *
from dataclasses import dataclass, field
from seguridad.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)
from autorizacion.seedwork.aplicacion.comandos import Comando

class ComandoCrearAnonimizacionPayload(ComandoIntegracion):
    fecha_creacion  = String()
    fecha_actualizacion = String()
    id = String()
    nombre = String()
    imagen = String()
    fecha_fin = String()

class ComandoCrearAnonimizacion(ComandoIntegracion):
    data = ComandoCrearAnonimizacionPayload()


@dataclass
class CrearAnonimizacion(Comando):
    fecha_creacion: str
    fecha_actualizacion: str
    id: str
    nombre: str
    imagen: str
    fecha_fin: str

################################################################
class ComandoError_AnonimizacionPayload(ComandoIntegracion):
    imagen = String()

class ComandoError_Anonimizacion(ComandoIntegracion):
    data = ComandoError_AnonimizacionPayload()

@dataclass
class Error_Anonimizacion(Comando):
    imagen: str
################################################################