from pulsar.schema import *
from ingestion_datos.utils import time_millis
import uuid

class IngestionFinalizada(Record):
    id = String(),
    id_correlacion = String(),
    ingestion_id = String()
    fecha_creacion = String()
    imagen = String()
    nombre = String()
 
class IngestionCancelada(Record):
    id = String()
    id_correlacion = String()
    ingestion_id = String()
    fecha_actualizacion = String()

class EventoIngestion(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="EventoIngestion")
    datacontenttype = String()
    service_name = String(default="ingestion-datos.Saludtech")
    ingestion_finalizada = IngestionFinalizada
    ingestion_cancelada = IngestionCancelada

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
