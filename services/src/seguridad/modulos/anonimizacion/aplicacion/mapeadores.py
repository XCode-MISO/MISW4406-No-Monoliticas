from seguridad.seedwork.aplicacion.dto import Mapeador as AppMap
from seguridad.seedwork.dominio.repositorios import Mapeador as RepMap
from seguridad.modulos.anonimizacion.dominio.entidades import Anonimizacion
from .dto import AnonimizacionDTO

from datetime import datetime


class MapeadorAnonimizacionDTOJson(AppMap):
    def externo_a_dto(self, externo: dict) -> AnonimizacionDTO:
        return AnonimizacionDTO(
            fecha_creacion=externo.get('fecha_creacion'),
            fecha_actualizacion=externo.get('fecha_actualizacion'),
            fecha_fin=externo.get('fecha_fin'),
            imagen=externo.get('imagen')
        )
    def dto_a_externo(self, dto: AnonimizacionDTO) -> dict:
        return dto.__dict__


class MapeadorAnonimizacion(RepMap):
    def entidad_a_dto(self, entidad: Anonimizacion) -> AnonimizacionDTO:
        fecha_creacion = entidad.fecha_creacion.strftime(self._FORMATO_FECHA)
        fecha_actualizacion = entidad.fecha_actualizacion.strftime(
            self._FORMATO_FECHA)
        fecha_fin = entidad.fecha_fin.strftime(self._FORMATO_FECHA)
        _id = str(entidad.id)
        imagen = str(entidad.image)
        return AnonimizacionDTO(
            fecha_creacion=fecha_creacion,
            fecha_actualizacion=fecha_actualizacion,
            fecha_fin=fecha_fin,
            imagen=imagen)
    def dto_a_entidad(self, entidad: AnonimizacionDTO) -> Anonimizacion:
        return Anonimizacion(
            _id=entidad.id,
            fecha_actualizacion=entidad.fecha_actualizacion,
            fecha_creacion=entidad.fecha_creacion,
            fecha_fin=entidad.fecha_fin,
            image=entidad.image
        )