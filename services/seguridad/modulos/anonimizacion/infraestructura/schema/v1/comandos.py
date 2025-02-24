from pulsar.schema import *
from dataclasses import dataclass, field
from seguridad.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoCrearAnonimizacionPayload(ComandoIntegracion):
    fecha_creacion  = String()
    fecha_actualizacion = String()
    id = String()
    nombre = String()
    imagen = String()
    fecha_fin = String()

class ComandoCrearAnonimizacion(ComandoIntegracion):
    data = ComandoCrearAnonimizacionPayload()