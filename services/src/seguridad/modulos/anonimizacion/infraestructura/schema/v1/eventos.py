from pulsar.schema import *

from seguridad.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class AnonimizacionCreadaPayload(Record):
    id_reserva = String()
    id_cliente = String()
    estado = String()
    fecha_creacion = Long()

class EventoAnonimizacionCreada(EventoIntegracion):
    data = AnonimizacionCreadaPayload()