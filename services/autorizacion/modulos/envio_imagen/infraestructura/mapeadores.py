""" Mapeadores para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from autorizacion.seedwork.dominio.repositorios import Mapeador
from autorizacion.modulos.envio_imagen.dominio.entidades import ValidacionEnvio_Imagen
from .dto import ValidacionEnvio_Imagen as ValidacionEnvio_ImagenDTO


class MapeadorValidacionEnvio_Imagen(Mapeador):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return ValidacionEnvio_Imagen.__class__

    def entidad_a_dto(self, entidad: ValidacionEnvio_Imagen) -> ValidacionEnvio_ImagenDTO:

        validacion_envio_imagen_dto = ValidacionEnvio_ImagenDTO(
            fecha_validacion = entidad.fecha_validacion,
            fecha_actualizacion = entidad.fecha_actualizacion,
            id = str(entidad.id),
            imagen = str(entidad.image),
            estado = str(entidad.estado)
        )
        print("entidad a dto")
        print(str(entidad.id))
        print(validacion_envio_imagen_dto)

        return validacion_envio_imagen_dto

    def dto_a_entidad(self, dto: ValidacionEnvio_ImagenDTO) -> ValidacionEnvio_Imagen:
        ValidacionEnvio_Imagen = ValidacionEnvio_Imagen(
            id=dto.id,
            fecha_validacion=dto.fecha_validacion,
            fecha_actualizacion=dto.fecha_actualizacion,
            imagen=dto.imagen,
            estado=dto.estado
        )

        return ValidacionEnvio_Imagen
