from pulsar.schema import *
from autorizacion.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class Validacion_UsuarioAgregadaPayload(Record):
    id_validacion_usuario = String()
    estado = String()
    fecha_validacion = Long()

class Validacion_UsuarioAgregada(EventoIntegracion):
    data = Validacion_UsuarioAgregadaPayload()

    def __init__(self, *args, **kwargs):    
        super().__init__(*args, **kwargs)

class Validacion_UsuarioFinalizada(Record):
     id = String()
     id_correlacion = String()
     ingestion_id = String()
     imagen = String()
     nombre = String()
     fecha_creacion = String()

class ErrorValidacion_Usuario(Record):
     nombre = String()

