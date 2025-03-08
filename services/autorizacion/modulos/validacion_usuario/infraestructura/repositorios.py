""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de vuelos

"""
from autorizacion.config.db import db
from autorizacion.modulos.validacion_usuario.dominio.repositorios import RepositorioValidacion_Usuario,RepositorioUsuario
from autorizacion.modulos.validacion_usuario.dominio.entidades import Validacion_Usuario, Usuario
from autorizacion.modulos.validacion_usuario.dominio.fabricas import FabricaValidacion_Usuario, FabricaUsuario
from .dto import Validacion_Usuario as Validacion_UsuarioDTO, Usuario as UsuarioDTO
from .mapeadores import MapeadorValidacion_Usuario, MapeadorUsuario
from uuid import UUID

class RepositorioValidacion_UsuarioMYSQL(RepositorioValidacion_Usuario):

    def __init__(self):
        self._fabrica_validacion_usuario: FabricaValidacion_Usuario = FabricaValidacion_Usuario()

    @property
    def fabrica_validacion_usuario(self):
        return self._fabrica_validacion_usuario

    def obtener_por_id(self, id: UUID) -> Validacion_Usuario:
        validacion_usuario_dto = db.session.query(Validacion_UsuarioDTO).filter_by(id=str(id)).first()
        return self.fabrica_validacion_usuario.crear_objeto(validacion_usuario_dto, MapeadorValidacion_Usuario())

    def obtener_todos(self) -> list[Validacion_Usuario]:
        validacion_usuario_dto = db.session.query(Validacion_UsuarioDTO).all()
        validacion_usuario: list[Validacion_UsuarioDTO]=list()
            
        for validacion_usuario in validacion_usuario_dto:    
            validacion_usuario.append(self.fabrica_validacion_usuario.crear_objeto(validacion_usuario, MapeadorValidacion_Usuario()))

        return validacion_usuario
    
    def agregar(self, validacion_usuario: Validacion_Usuario):
        try:
            validacion_usuario_dto = self.fabrica_validacion_usuario.crear_objeto(validacion_usuario, MapeadorValidacion_Usuario())
            db.session.add(validacion_usuario_dto)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print('Error al agregar la validacion_usuario:', e)

    def actualizar(self, reserva: Validacion_Usuario):
        # TODO
        raise NotImplementedError

    def eliminar(self, usuario: str):
        try:
            db.session.query(Validacion_UsuarioDTO).filter_by(usuario=usuario).delete()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f'Error al eliminar la validación del usuario {usuario}: {e}')
        #raise NotImplementedError
    
#######################################################****************************************############################################
    
class RepositorioUsuarioMYSQL(RepositorioUsuario):

    def __init__(self):
        self._fabrica_usuario: FabricaUsuario = FabricaUsuario()

    @property
    def fabrica_usuario(self):
        return self._fabrica_usuario

    def obtener_por_id(self, id: UUID) -> Usuario:
        usuario_dto = db.session.query(UsuarioDTO).filter_by(id=str(id)).first()
        return self.fabrica_usuario.crear_objeto(usuario_dto, MapeadorUsuario())

    def obtener_todos(self) -> list[Usuario]:
        usuario_dto = db.session.query(UsuarioDTO).all()
        usuario: list[UsuarioDTO]=list()
            
        for usuario in usuario_dto:    
            usuario.append(self.fabrica_usuario.crear_objeto(usuario, MapeadorUsuario()))

        return usuario
    
    def agregar(self, usuario: Validacion_Usuario):
        try:
            usuario_dto = self.fabrica_usuario.crear_objeto(usuario, MapeadorUsuario())
            db.session.add(usuario_dto)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print('Error al agregar la usuario:', e)

    def actualizar(self, reserva: Usuario):
        # TODO
        raise NotImplementedError

    def eliminar(self, reserva_id: UUID):
        # TODO
        raise NotImplementedError