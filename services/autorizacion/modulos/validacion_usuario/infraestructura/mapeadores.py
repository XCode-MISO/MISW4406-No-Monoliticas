""" Mapeadores para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""
from autorizacion.seedwork.dominio.repositorios import Mapeador
from autorizacion.modulos.validacion_usuario.dominio.entidades import Validacion_Usuario, Usuario
from .dto import Validacion_Usuario as Validacion_UsuarioDTO, Usuario as UsuarioDTO

class MapeadorValidacion_Usuario(Mapeador):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return Validacion_Usuario.__class__

    def entidad_a_dto(self, entidad: Validacion_Usuario) -> Validacion_UsuarioDTO:
        validacion_usuario_dto = Validacion_UsuarioDTO()
        validacion_usuario_dto.fecha_validacion = entidad.fecha_validacion
        validacion_usuario_dto.fecha_actualizacion = entidad.fecha_actualizacion
        validacion_usuario_dto.id = str(entidad.id)
        validacion_usuario_dto.usuario = entidad.usuario
        validacion_usuario_dto.imagen = entidad.imagen
        return validacion_usuario_dto

    def dto_a_entidad(self, dto: Validacion_UsuarioDTO) -> Validacion_Usuario:
        validacion_usuario = Validacion_Usuario( dto.fecha_validacion, dto.fecha_actualizacion, dto.id, dto.usuario, dto.imagen)
        return validacion_usuario
        
class MapeadorUsuario(Mapeador):

    def obtener_tipo(self) -> type:
        return Usuario.__class__

    def entidad_a_dto(self, entidad: Usuario) -> UsuarioDTO:
        usuario_dto = UsuarioDTO()
        usuario_dto.id = str(entidad.id)
        usuario_dto.usuario = entidad.usuario
        return usuario_dto

    def dto_a_entidad(self, dto: Validacion_UsuarioDTO) -> Validacion_Usuario:
        validacion_usuario = Validacion_Usuario( dto.fecha_validacion, dto.fecha_actualizacion, dto.id, dto.usuario, dto.imagen)
        return validacion_usuario