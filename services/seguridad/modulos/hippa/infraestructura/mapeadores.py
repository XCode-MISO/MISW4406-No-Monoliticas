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

        validacion_hippa_dto = ValidacionHippaDTO(
            fecha_creacion = entidad.fecha_creacion,
            fecha_actualizacion = entidad.fecha_actualizacion,
            id = str(entidad.id),
            imagen = str(entidad.image),
            estado = str(entidad.estado)
        )
        print("entidad a dto")
        print(str(entidad.id))
        print(validacion_hippa_dto)

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
