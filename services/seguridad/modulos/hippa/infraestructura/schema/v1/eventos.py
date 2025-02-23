from pulsar.schema import *

from seguridad.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class ValidacionHippaPayload(Record):
    id_reserva = String()
    id_cliente = String()
    estado = String()
    fecha_creacion = Long()

class EventoValidacionHippaCreada(EventoIntegracion):
    data = ValidacionHippaPayload()