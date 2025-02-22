from pda.seedwork.aplicacion.servicios import Servicio
from pda.modulos.anonimizacion.dominio.entidades import Anonimizacion
from pda.modulos.anonimizacion.dominio.fabricas import FabricaAnonimizacion
from pda.modulos.anonimizacion.infraestructura.fabricas import FabricaRepositorio
from pda.modulos.anonimizacion.infraestructura.repositorios import RepositorioReservas
from pda.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from .mapeadores import MapeadorReserva
from .dto import AnonimizacionDTO
import asyncio

class ServicioAnonimizacion(Servicio):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_vuelos: FabricaAnonimizacion = FabricaAnonimizacion()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_anonimizaciones(self):
        return self._fabrica_anonimizaciones       
    
    def crear_anonimizacion(self, anonimizacion_dto: AnonimizacionDTO) -> AnonimizacionDTO:
        anonimizacion: Anonimizacion = self.fabrica_anonimizaciones.crear_objeto(anonimizacion_dto, MapeadorReserva())
        anonimizacion.crear_anonimizacion(anonimizacion)
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioReservas.__class__)
        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, anonimizacion)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()
        return self.fabrica_anonimizaciones.crear_objeto(anonimizacion, MapeadorReserva())

    def obtener_anonimizacion_por_id(self, id) -> AnonimizacionDTO:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioReservas.__class__)
        return self.fabrica_anonimizaciones.crear_objeto(repositorio.obtener_por_id(id), MapeadorReserva())
