from tokenize import String
from pulsar.schema import *
from dataclasses import dataclass, field
from seguridad.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoCrearValidacionHippaPayload(ComandoIntegracion):
    id = String()
    image = String()
    estado = String()

class ComandoCrearValidacionHippa(ComandoIntegracion):
    data = ComandoCrearValidacionHippaPayload()