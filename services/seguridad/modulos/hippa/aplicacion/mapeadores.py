from seguridad.seedwork.aplicacion.dto import Mapeador as AppMap
from seguridad.seedwork.dominio.repositorios import Mapeador as RepMap
from seguridad.modulos.hippa.dominio.entidades import ValidacionHippa
from .dto import ImagenHippaDTO

from datetime import datetime


class MapeadorImagenHippaDTOJson(AppMap):
    def externo_a_dto(self, externo: dict) -> ImagenHippaDTO:
        return ImagenHippaDTO(
            fecha_creacion=externo.get('fecha_creacion'),
            fecha_actualizacion=externo.get('fecha_actualizacion'),
            fecha_fin=externo.get('fecha_fin'),
            imagen=externo.get('imagen')
        )
    def dto_a_externo(self, dto: ImagenHippaDTO) -> dict:
        return dto.__dict__


class MapeadorValidacionHippa(RepMap):
    def entidad_a_dto(self, entidad: ValidacionHippa) -> ImagenHippaDTO:
        fecha_creacion = entidad.fecha_creacion.strftime(self._FORMATO_FECHA)
        fecha_actualizacion = entidad.fecha_actualizacion.strftime(
            self._FORMATO_FECHA)
        fecha_fin = entidad.fecha_fin.strftime(self._FORMATO_FECHA)
        _id = str(entidad.id)
        imagen = str(entidad.image)
        estado = str(entidad.estado)
        return ImagenHippaDTO(
            fecha_creacion=fecha_creacion,
            fecha_actualizacion=fecha_actualizacion,
            fecha_fin=fecha_fin,
            imagen=imagen,
            estado=estado
            )
    def dto_a_entidad(self, entidad: ImagenHippaDTO) -> ValidacionHippa:
        return ValidacionHippa(
            _id=entidad.id,
            fecha_actualizacion=entidad.fecha_actualizacion,
            fecha_creacion=entidad.fecha_creacion,
            fecha_fin=entidad.fecha_fin,
            image=entidad.image,
            estado=entidad.estado
        )