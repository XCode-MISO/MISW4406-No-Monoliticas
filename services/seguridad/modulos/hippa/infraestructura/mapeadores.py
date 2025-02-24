""" Mapeadores para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from seguridad.seedwork.dominio.repositorios import Mapeador
from seguridad.modulos.hippa.dominio.entidades import ValidacionHippa
from .dto import ValidacionHippa as ValidacionHippaDTO


class MapeadorValidacionHippa(Mapeador):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return ValidacionHippa.__class__

    def entidad_a_dto(self, entidad: ValidacionHippa) -> ValidacionHippaDTO:

        validacion_hippa_dto = ValidacionHippaDTO()
        validacion_hippa_dto.fecha_creacion = entidad.fecha_creacion
        validacion_hippa_dto.fecha_actualizacion = entidad.fecha_actualizacion
        validacion_hippa_dto.id = str(entidad.id)
        validacion_hippa_dto.imagen = str(entidad.image)
        validacion_hippa_dto.estado = str(entidad.estado)

        return validacion_hippa_dto

    def dto_a_entidad(self, dto: ValidacionHippaDTO) -> ValidacionHippa:
        ValidacionHippa = ValidacionHippa(
            id=dto.id,
            fecha_creacion=dto.fecha_creacion,
            fecha_actualizacion=dto.fecha_actualizacion,
            imagen=dto.imagen,
            estado=dto.estado
        )

        return ValidacionHippa
