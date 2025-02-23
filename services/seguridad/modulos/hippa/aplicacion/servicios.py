from seguridad.seedwork.aplicacion.servicios import Servicio
from seguridad.modulos.hippa.dominio.entidades import ValidacionHippa
from seguridad.modulos.hippa.dominio.fabricas import FabricaValidacionHippa
from seguridad.modulos.hippa.infraestructura.fabricas import FabricaRepositorio
from seguridad.modulos.hippa.infraestructura.repositorios import RepositorioReservas
from seguridad.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from .mapeadores import MapeadorReserva
from .dto import ValidacionHippaDTO
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
    
    def crear_validacion_hippa(self, validation_hippa_dto: ValidacionHippaDTO) -> ValidacionHippaDTO:
        validacion_hippa: ValidacionHippa = self.fabrica_validacion_hippa.crear_objeto(validation_hippa_dto, MapeadorReserva())
        validacion_hippa.crear_validacion_hippa(validacion_hippa)
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioReservas.__class__)
        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, validacion_hippa)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()
        return self.fabrica_validacion_hippaes.crear_objeto(validacion_hippa, MapeadorReserva())

    def obtener_validacion_hippa_por_id(self, id) -> ValidacionHippaDTO:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioReservas.__class__)
        return self.fabrica_validacion_hippaes.crear_objeto(repositorio.obtener_por_id(id), MapeadorReserva())
