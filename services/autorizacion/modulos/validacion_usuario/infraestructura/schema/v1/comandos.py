from pulsar.schema import *
from dataclasses import dataclass, field
from autorizacion.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

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