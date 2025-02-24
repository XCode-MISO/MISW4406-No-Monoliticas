from pulsar.schema import *

from seguridad.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class ValidacionHippaPayload(Record):
    id = String()
    estado = String()
    imagen = String()

class EventoValidacionHippaCreada(EventoIntegracion):
    data = ValidacionHippaPayload()