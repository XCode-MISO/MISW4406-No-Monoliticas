from pulsar.schema import *
from dataclasses import dataclass, field
from seguridad.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoCrearAnonimizacionPayload(ComandoIntegracion):
    id_usuario = String()
    # TODO Cree los records para itinerarios

class ComandoCrearAnonimizacion(ComandoIntegracion):
    data = ComandoCrearAnonimizacionPayload()