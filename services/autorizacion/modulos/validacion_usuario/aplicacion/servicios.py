from autorizacion.seedwork.aplicacion.servicios import Servicio
from autorizacion.modulos.validacion_usuario.dominio.entidades import Validacion_Usuario
from autorizacion.modulos.validacion_usuario.dominio.fabricas import FabricaValidacion_Usuario
from autorizacion.modulos.validacion_usuario.infraestructura.fabricas import FabricaRepositorio
from autorizacion.modulos.validacion_usuario.infraestructura.repositorios import RepositorioValidacion_Usuario
from .mapeadores import MapeadorValidacion_Usuario

from .dto import Validacion_UsuarioDTO

class ServicioValidacion_Usuario(Servicio):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_validacion_usuario: FabricaValidacion_Usuario = FabricaValidacion_Usuario()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_validacion_usuario(self):
        return self._fabrica_validacion_usuario

    def crear_validacion_usuario(self, validacion_usuario_dto: Validacion_UsuarioDTO) -> Validacion_UsuarioDTO:
        validacion_usuario: Validacion_Usuario = self.fabrica_validacion_usuario.crear_objeto(validacion_usuario_dto, MapeadorValidacion_Usuario())
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioValidacion_Usuario.__class__)
        repositorio.agregar(validacion_usuario)
        return self.fabrica_validacion_usuario.crear_objeto(validacion_usuario, MapeadorValidacion_Usuario())

    def borrar_usuario_maligno(self, nombre: str) -> None:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioValidacion_Usuario.__class__)
        repositorio.eliminar("maligno")

    def obtener_validacion_usuario_por_id(self, id) -> Validacion_UsuarioDTO:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioValidacion_Usuario.__class__)
        return repositorio.obtener_por_id(id).__dict__
    
    def obtener_todas_las_validacion_usuario(self) -> list[Validacion_UsuarioDTO]:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioValidacion_Usuario.__class__)
        validacion_usuario = repositorio.obtener_todos()
        mapeador = MapeadorValidacion_Usuario()
        validacion_usuario_dto = [mapeador.entidad_a_dto(validacion_usuario) for validacion_usuario in validacion_usuario]
        return validacion_usuario_dto
    