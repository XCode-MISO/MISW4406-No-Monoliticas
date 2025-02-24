from pulsar.schema import *
from dataclasses import dataclass, field
from seguridad.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoCrearAnonimizacionPayload(ComandoIntegracion):
    id = String()

class ComandoCrearAnonimizacion(ComandoIntegracion):
    data = ComandoCrearAnonimizacionPayload()