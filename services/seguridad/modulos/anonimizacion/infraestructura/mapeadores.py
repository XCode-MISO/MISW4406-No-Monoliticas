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
        print(f"ANONIMIZACION PARA BASE DE DATOS: {entidad}")
        anonimizacion_dto = AnonimizacionDTO()
        anonimizacion_dto.fecha_creacion = entidad.fecha_creacion
        anonimizacion_dto.fecha_actualizacion = entidad.fecha_actualizacion
        anonimizacion_dto.id = str(entidad.id)
        anonimizacion_dto.nombre = entidad.nombre
        anonimizacion_dto.imagen = entidad.imagen
        anonimizacion_dto.fecha_fin = entidad.fecha_fin
        return anonimizacion_dto

    def dto_a_entidad(self, dto: AnonimizacionDTO) -> Anonimizacion:
        anonimizacion = Anonimizacion(dto.id, dto.fecha_creacion, dto.fecha_actualizacion, dto.nombre, dto.imagen, dto.fecha_fin)
        return anonimizacion