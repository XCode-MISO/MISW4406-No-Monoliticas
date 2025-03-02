import logging
import traceback
from abc import ABC, abstractmethod

from seguridad.seedwork.infraestructura.proyecciones import Proyeccion, ProyeccionHandler
from seguridad.seedwork.infraestructura.proyecciones import ejecutar_proyeccion as projection
from seguridad.seedwork.infraestructura.utils import millis_a_datetime
from ingestion_datos.infraestructura.dto import IngestionDatosAnalitica


class IngestionDatosProjection(Proyeccion, ABC):
    @abstractmethod
    def ejecutar(self): ...


class TotalIngestionDatosProjection(IngestionDatosProjection):
    ADD = 1
    DELETE = 2
    UPDATE = 3

    def __init__(self, fecha_creacion, operation):
        self.fecha_creacion = millis_a_datetime(fecha_creacion)
        self.operation = operation

    def ejecutar(self, db=None):
        if not db:
            logging.error("ERROR: application DB cannot be null")
            return
        record = (
            db.query(IngestionDatosAnalitica)
            .filter_by(fecha_creacion=self.fecha_creacion.date())
            .one_or_none()
        )

        if record and self.operation == self.ADD:
            record.total += 1
        elif record and self.operation == self.DELETE:
            record.total -= 1
            record.total = max(record.total, 0)
        else:
            db.add(
                IngestionDatosAnalitica(fecha_creacion=self.fecha_creacion.date(), total=1)
            )

        db.commit()

class IngestionDatosProjectionHandler(ProyeccionHandler):
    def handle(self, projection: IngestionDatosProjection):
        from ingestion_datos.config.db import get_db
        db = next(get_db())
        projection.ejecutar(db=db)

@projection.register(TotalIngestionDatosProjection)
def execute_transaction_projection(projection):
    handler = IngestionDatosProjectionHandler()
    handler.handle(projection)
