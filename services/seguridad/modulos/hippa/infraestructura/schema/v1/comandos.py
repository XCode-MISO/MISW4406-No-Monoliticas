from tokenize import String
from pulsar.schema import *
from dataclasses import dataclass, field
from seguridad.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoCrearValidacionHippaPayload(ComandoIntegracion):
    id = String()
    image = String()
    estado = String()
    fecha_actualizacion = String()
    fecha_creacion = String()
class ComandoCrearValidacionHippa(ComandoIntegracion):
    data = ComandoCrearValidacionHippaPayload()