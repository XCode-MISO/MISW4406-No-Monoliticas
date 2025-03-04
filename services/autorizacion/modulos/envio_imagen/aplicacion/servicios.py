from autorizacion.seedwork.aplicacion.servicios import Servicio
from autorizacion.modulos.envio_imagen.dominio.entidades import ValidacionEnvio_Imagen
from autorizacion.modulos.envio_imagen.dominio.fabricas import FabricaValidacionEnvio_Imagen
from autorizacion.modulos.envio_imagen.infraestructura.fabricas import FabricaRepositorio
from autorizacion.modulos.envio_imagen.infraestructura.repositorios import RepositorioValidacionesEnvio_Imagen
from .mapeadores import MapeadorValidacionEnvio_Imagen

from .dto import ImagenEnvio_ImagenDTO

class ServicioValidacionEnvio_Imagen(Servicio):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_validacion_envio_imagen: FabricaValidacionEnvio_Imagen = FabricaValidacionEnvio_Imagen()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_validacion_envio_imagen(self):
        return self._fabrica_validacion_envio_imagen       
    
    def crear_validacion_envio_imagen(self, validation_envio_imagen_dto: ImagenEnvio_ImagenDTO) -> ImagenEnvio_ImagenDTO:
        validacion_envio_imagen: ValidacionEnvio_Imagen = self.fabrica_validacion_envio_imagen.crear_objeto(validation_envio_imagen_dto, MapeadorValidacionEnvio_Imagen())
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioValidacionesEnvio_Imagen.__class__)
        repositorio.agregar(validacion_envio_imagen)
        """ UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, validacion_envio_imagen)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit() """
        return self.fabrica_validacion_envio_imagen.crear_objeto(validacion_envio_imagen, MapeadorValidacionEnvio_Imagen())

    def obtener_validacion_envio_imagen_por_id(self, id) -> ImagenEnvio_ImagenDTO:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioValidacionesEnvio_Imagen.__class__)
        return repositorio.obtener_por_id(id).__dict__   
    
    def obtener_todas_las_validacion_usuario(self) -> list[ImagenEnvio_ImagenDTO]:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioValidacionesEnvio_Imagen.__class__)
        validacion_usuario = repositorio.obtener_todos()
        mapeador = MapeadorValidacionEnvio_Imagen()
        validacion_usuario_dto = [mapeador.entidad_a_dto(validacion_usuario) for validacion_usuario in validacion_usuario]
        return validacion_usuario_dto
    