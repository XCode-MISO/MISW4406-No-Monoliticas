from autorizacion.seedwork.aplicacion.dto import Mapeador as AppMap
from autorizacion.seedwork.dominio.repositorios import Mapeador as RepMap
from autorizacion.modulos.validacion_usuario.dominio.entidades import Validacion_Usuario
from .dto import Validacion_UsuarioDTO

from datetime import datetime

class MapeadorValidacion_UsuarioDTOJson(AppMap):
    def externo_a_dto(self, externo: dict) -> Validacion_UsuarioDTO:
        validacion_usuario_dto = Validacion_UsuarioDTO(
            externo.get('fecha_actualizacion'),
            externo.get('fecha_validacion'),
            externo.get('id'),
            externo.get('usuario'),
            externo.get('nombre'),
            externo.get('imagen'),
            externo.get('fecha_fin'))
        return validacion_usuario_dto

    def dto_a_externo(self, dto: Validacion_UsuarioDTO) -> dict:
        return dto.__dict__

class MapeadorValidacion_Usuario(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return Validacion_Usuario.__class__

    def entidad_a_dto(self, entidad: Validacion_Usuario) -> Validacion_UsuarioDTO:
        fecha_validacion = entidad.fecha_validacion.strftime(self._FORMATO_FECHA)
        fecha_actualizacion = entidad.fecha_actualizacion.strftime(self._FORMATO_FECHA)
        _id = str(entidad.id)
        usuario = entidad.usuario
        nombre = entidad.nombre
        imagen = entidad.imagen
        fecha_fin = entidad.fecha_fin
        return Validacion_UsuarioDTO(fecha_validacion, fecha_actualizacion, _id, usuario, nombre, imagen, fecha_fin)

    def dto_a_entidad(self, dto: Validacion_UsuarioDTO) -> Validacion_Usuario:
        validacion_usuario = Validacion_Usuario()
        validacion_usuario.usuario = dto.usuario
        validacion_usuario.nombre = dto.nombre
        validacion_usuario.imagen = dto.imagen
        validacion_usuario.fecha_fin = dto.fecha_fin
        return validacion_usuario