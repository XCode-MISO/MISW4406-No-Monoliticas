import uuid
from autorizacion.seedwork.aplicacion.dto import Mapeador as AppMap
from autorizacion.seedwork.dominio.repositorios import Mapeador as RepMap
from autorizacion.modulos.envio_imagen.dominio.entidades import ValidacionEnvio_Imagen
from .dto import ImagenEnvio_ImagenDTO

from datetime import datetime
import logging

class MapeadorImagenEnvio_ImagenDTOJson(AppMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'
    def externo_a_dto(self, externo: dict) -> ImagenEnvio_ImagenDTO:
        return ImagenEnvio_ImagenDTO(
            imagen=externo.get('imagen'),
            id=externo.get('id', f'{uuid.uuid4()}'),
            fecha_validacion=externo.get('fecha_validacion', datetime.now().strftime(self._FORMATO_FECHA)),
            fecha_actualizacion=externo.get('fecha_actualizacion', datetime.now().strftime(self._FORMATO_FECHA)),
            estado=None,
        )
    def dto_a_externo(self, dto: ImagenEnvio_ImagenDTO) -> dict:
        return dto.__dict__


class MapeadorValidacionEnvio_Imagen(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'
    def obtener_tipo(self) -> type:
        return ValidacionEnvio_Imagen.__class__

    def entidad_a_dto(self, entidad: ValidacionEnvio_Imagen) -> ImagenEnvio_ImagenDTO:
        logging.debug(entidad)
        fecha_validacion = str(entidad.fecha_validacion)
        fecha_actualizacion = str(entidad.fecha_actualizacion)
        _id = str(entidad.id)
        imagen = str(entidad.image)
        estado = str(entidad.estado)
        return ImagenEnvio_ImagenDTO(_id,
            fecha_validacion=fecha_validacion,
            fecha_actualizacion=fecha_actualizacion,
            imagen=imagen,
            estado=estado
            )
    def dto_a_entidad(self, dto: ImagenEnvio_ImagenDTO) -> ValidacionEnvio_Imagen:
        validacionEnvio_Imagen = ValidacionEnvio_Imagen(
            id=dto.id,
            fecha_validacion=datetime.strptime(dto.fecha_validacion, self._FORMATO_FECHA),
            fecha_actualizacion=datetime.strptime(dto.fecha_actualizacion, self._FORMATO_FECHA),
            image=dto.imagen,
            estado=None,
        )
        
        return validacionEnvio_Imagen