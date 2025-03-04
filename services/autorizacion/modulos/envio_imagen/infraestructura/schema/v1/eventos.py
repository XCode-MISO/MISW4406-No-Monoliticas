from pulsar.schema import *

from autorizacion.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class ValidacionEnvio_ImagenPayload(Record):
    id = String()
    estado = String()
    image = String()

class EventoValidacionEnvio_ImagenCreada(EventoIntegracion):
    data = ValidacionEnvio_ImagenPayload()