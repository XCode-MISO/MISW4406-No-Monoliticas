from seguridad.seedwork.aplicacion.servicios import Servicio
from seguridad.modulos.hippa.dominio.entidades import ValidacionHippa
from seguridad.modulos.hippa.dominio.fabricas import FabricaValidacionHippa
from seguridad.modulos.hippa.infraestructura.fabricas import FabricaRepositorio
from seguridad.modulos.hippa.infraestructura.repositorios import RepositorioValidacionesHippa
from seguridad.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from .mapeadores import MapeadorValidacionHippa
from .dto import ImagenHippaDTO
import asyncio

class ServicioValidacionHippa(Servicio):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_validacion_hippa: FabricaValidacionHippa = FabricaValidacionHippa()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_validacion_hippa(self):
        return self._fabrica_validacion_hippa       
    
    def crear_validacion_hippa(self, validation_hippa_dto: ImagenHippaDTO) -> ImagenHippaDTO:
        validacion_hippa: ValidacionHippa = self.fabrica_validacion_hippa.crear_objeto(validation_hippa_dto, MapeadorValidacionHippa())
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioValidacionesHippa.__class__)
        """ UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, validacion_hippa)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit() """
        return self.fabrica_validacion_hippa.crear_objeto(validacion_hippa, MapeadorValidacionHippa())

    def obtener_validacion_hippa_por_id(self, id) -> ImagenHippaDTO:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioValidacionesHippa.__class__)
        return self.fabrica_validacion_hippa.crear_objeto(repositorio.obtener_por_id(id), MapeadorValidacionHippa())
