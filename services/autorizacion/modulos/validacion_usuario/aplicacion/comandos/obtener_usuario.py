from autorizacion.seedwork.aplicacion.comandos import Comando
from autorizacion.modulos.validacion_usuario.aplicacion.dto import Validacion_UsuarioDTO
from .base import CrearValidacion_UsuarioBaseHandler
from dataclasses import dataclass, field
from autorizacion.seedwork.aplicacion.comandos import ejecutar_commando as comando

from autorizacion.modulos.validacion_usuario.dominio.entidades import Validacion_Usuario
from autorizacion.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from autorizacion.modulos.validacion_usuario.aplicacion.mapeadores import MapeadorValidacion_Usuario
from autorizacion.modulos.validacion_usuario.infraestructura.repositorios import RepositorioValidacion_Usuario

@dataclass
class Crear_Usuario(Comando):
    id: str
    usuario: str
    


class CrearValidacion_UsuarioHandler(CrearValidacion_UsuarioBaseHandler):
    
    def handle(self, comando: Crear_Usuario):
        validacion_usuario_dto = Validacion_UsuarioDTO(
                fecha_actualizacion=comando.fecha_actualizacion
            ,   fecha_validacion=comando.fecha_validacion
            ,   id=comando.id
            ,   usuario=comando.usuario
            ,   nombre=comando.id
            ,   imagen=comando.id
            ,   fecha_fin=comando.id)

        validacion_usuario: Validacion_Usuario = self.fabrica_validacion_usuario.crear_objeto(validacion_usuario_dto, MapeadorValidacion_Usuario())
        validacion_usuario.crear_validacion_usuario(validacion_usuario)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioValidacion_Usuario.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, validacion_usuario)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(CrearValidacion_Usuario)
def ejecutar_comando_crear_validacion_usuario(comando: CrearValidacion_Usuario):
    handler = CrearValidacion_UsuarioHandler()
    handler.handle(comando)