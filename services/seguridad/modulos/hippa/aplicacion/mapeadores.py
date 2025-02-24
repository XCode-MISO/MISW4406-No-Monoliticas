import uuid
from seguridad.seedwork.aplicacion.dto import Mapeador as AppMap
from seguridad.seedwork.dominio.repositorios import Mapeador as RepMap
from seguridad.modulos.hippa.dominio.entidades import ValidacionHippa
from .dto import ImagenHippaDTO

from datetime import datetime
import logging

class MapeadorImagenHippaDTOJson(AppMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'
    def externo_a_dto(self, externo: dict) -> ImagenHippaDTO:
        return ImagenHippaDTO(
            imagen=externo.get('imagen'),
            id=externo.get('id', f'{uuid.uuid4()}'),
            fecha_creacion=externo.get('fecha_creacion', datetime.now().strftime(self._FORMATO_FECHA)),
            fecha_actualizacion=externo.get('fecha_actualizacion', datetime.now().strftime(self._FORMATO_FECHA)),
            estado=None,
        )
    def dto_a_externo(self, dto: ImagenHippaDTO) -> dict:
        return dto.__dict__


class MapeadorValidacionHippa(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'
    def obtener_tipo(self) -> type:
        return ValidacionHippa.__class__

    def entidad_a_dto(self, entidad: ValidacionHippa) -> ImagenHippaDTO:
        logging.debug(entidad)
        fecha_creacion = str(entidad.fecha_creacion)
        fecha_actualizacion = str(entidad.fecha_actualizacion)
        _id = str(entidad.id)
        imagen = str(entidad.image)
        estado = str(entidad.estado)
        return ImagenHippaDTO(_id,
            fecha_creacion=fecha_creacion,
            fecha_actualizacion=fecha_actualizacion,
            imagen=imagen,
            estado=estado
            )
    def dto_a_entidad(self, dto: ImagenHippaDTO) -> ValidacionHippa:
        validacionHippa = ValidacionHippa(
            id=dto.id,
            fecha_creacion=datetime.strptime(dto.fecha_creacion, self._FORMATO_FECHA),
            fecha_actualizacion=datetime.strptime(dto.fecha_actualizacion, self._FORMATO_FECHA),
            image=dto.imagen,
            estado=None,
        )
        
        return validacionHippa