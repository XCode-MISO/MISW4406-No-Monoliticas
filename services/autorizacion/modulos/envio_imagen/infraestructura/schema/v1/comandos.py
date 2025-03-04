from tokenize import String
from pulsar.schema import *
from dataclasses import dataclass, field
from autorizacion.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoCrearValidacionEnvio_ImagenPayload(ComandoIntegracion):
    id = String()
    image = String()
    estado = String()

class ComandoCrearValidacionEnvio_Imagen(ComandoIntegracion):
    data = ComandoCrearValidacionEnvio_ImagenPayload()