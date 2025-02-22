""" Mapeadores para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from seguridad.seedwork.dominio.repositorios import Mapeador
from seguridad.modulos.anonimizacion.dominio.entidades import Anonimizacion

from .dto import Anonimizacion as AnonimizacionDTO


class MapeadorAnonimizacion(Mapeador):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return Anonimizacion.__class__

    def entidad_a_dto(self, entidad: Anonimizacion) -> AnonimizacionDTO:

        Anonimizacion_dto = AnonimizacionDTO()
        Anonimizacion_dto.fecha_creacion = entidad.fecha_creacion
        Anonimizacion_dto.fecha_actualizacion = entidad.fecha_actualizacion
        Anonimizacion_dto.id = str(entidad.id)

        itinerarios_dto = list()

        for itinerario in entidad.itinerarios:
            itinerarios_dto.extend(self._procesar_itinerario(itinerario))

        Anonimizacion_dto.itinerarios = itinerarios_dto

        return Anonimizacion_dto

    def dto_a_entidad(self, dto: AnonimizacionDTO) -> Anonimizacion:
        Anonimizacion = Anonimizacion(
            id=dto.id,
            fecha_creacion=dto.fecha_creacion,
            fecha_actualizacion=dto.fecha_actualizacion,
            fecha_fin=dto.fecha_fin,
            imagen=dto.imagen
        )

        return Anonimizacion
