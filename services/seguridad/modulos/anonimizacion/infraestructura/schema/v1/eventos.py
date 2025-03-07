from pulsar.schema import *
from seguridad.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class AnonimizacionAgregadaPayload(Record):
    id_anonimizacion = String()
    estado = String()
    fecha_creacion = Long()
    imagen = String()
    nombre = String()

class AnonimizacionAgregada(EventoIntegracion):
    data = AnonimizacionAgregadaPayload()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)