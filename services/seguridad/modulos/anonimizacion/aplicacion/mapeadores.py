from seguridad.seedwork.aplicacion.dto import Mapeador as AppMap
from seguridad.seedwork.dominio.repositorios import Mapeador as RepMap
from seguridad.modulos.anonimizacion.dominio.entidades import Anonimizacion
from .dto import AnonimizacionDTO

from datetime import datetime

class MapeadorAnonimizacionDTOJson(AppMap):
    def externo_a_dto(self, externo: dict) -> AnonimizacionDTO:
        anonimizacion_dto = AnonimizacionDTO(externo.get('fecha_creacion'),externo.get('fecha_actualizacion'),'',externo.get('nombre'), externo.get('imagen'), externo.get('fecha_fin'))
        return anonimizacion_dto

    def dto_a_externo(self, dto: AnonimizacionDTO) -> dict:
        return dto.__dict__

class MapeadorAnonimizacion(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return 

    def entidad_a_dto(self, entidad: Anonimizacion) -> AnonimizacionDTO:
        fecha_creacion = entidad.fecha_creacion.strftime(self._FORMATO_FECHA)
        fecha_actualizacion = entidad.fecha_actualizacion.strftime(self._FORMATO_FECHA)
        _id = str(entidad.id)
        nombre = entidad.nombre
        imagen = entidad.imagen
        fecha_fin = entidad.fecha_fin
        return AnonimizacionDTO(fecha_creacion, fecha_actualizacion, _id, nombre, imagen, fecha_fin)

    def dto_a_entidad(self, dto: AnonimizacionDTO) -> Anonimizacion:
        anonimizacion = Anonimizacion()
        anonimizacion.nombre = dto.nombre
        anonimizacion.imagen = dto.imagen
        anonimizacion.fecha_fin = dto.fecha_fin
        return anonimizacion