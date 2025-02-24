import uuid
from seguridad.seedwork.aplicacion.dto import Mapeador as AppMap
from seguridad.seedwork.dominio.repositorios import Mapeador as RepMap
from seguridad.modulos.hippa.dominio.entidades import ValidacionHippa
from .dto import ImagenHippaDTO

from datetime import datetime
import logging

class MapeadorImagenHippaDTOJson(AppMap):
    def externo_a_dto(self, externo: dict) -> ImagenHippaDTO:
        return ImagenHippaDTO(
            imagen=externo.get('imagen'),
            id=externo.get('id', str(uuid.uuid4())),
        )
    def dto_a_externo(self, dto: ImagenHippaDTO) -> dict:
        return dto.__dict__


class MapeadorValidacionHippa(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return ValidacionHippa.__class__

    def entidad_a_dto(self, entidad: ValidacionHippa) -> ImagenHippaDTO:
        logging.debug(entidad)
        fecha_creacion = entidad.fecha_creacion.strftime(self._FORMATO_FECHA)
        fecha_actualizacion = entidad.fecha_actualizacion.strftime(
            self._FORMATO_FECHA)
        _id = str(entidad.id)
        imagen = str(entidad.image)
        estado = str(entidad.estado)
        return ImagenHippaDTO(
            fecha_creacion=fecha_creacion,
            fecha_actualizacion=fecha_actualizacion,
            imagen=imagen,
            estado=estado
            )
    def dto_a_entidad(self, entidad: ImagenHippaDTO) -> ValidacionHippa:
        return ValidacionHippa(
            id=entidad.id,
            fecha_creacion=datetime.now(),
            fecha_actualizacion=datetime.now(),
            image=entidad.imagen,
            estado=entidad.estado,
        )