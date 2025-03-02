from pulsar.schema import *
from ingestion_datos.utils import time_millis
import uuid

class IngestionDatosPayload(Record):
    id_correlacion = String(),
    imagen = String(),
    fecha_creacion = Long()
    nombre = String()
 
class RevertirIngestionDatosPayload(Record):
    id = String()
    id_correlacion = String()
    imagen = String()

class ComandoIngerirDatos(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="ComandoIngerirDatos")
    datacontenttype = String()
    service_name = String(default="ingestion-datos.Saludtech")
    data = IngestionDatosPayload

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ComandoRevertirIngestionDatos(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="RevertirIngestionDatos")
    datacontenttype = String()
    service_name = String(default="ingestion-datos.saludtech")
    data = RevertirIngestionDatosPayload

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
