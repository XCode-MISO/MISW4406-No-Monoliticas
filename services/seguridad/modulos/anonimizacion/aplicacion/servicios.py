from seguridad.seedwork.aplicacion.servicios import Servicio
from seguridad.modulos.anonimizacion.dominio.entidades import Anonimizacion
from seguridad.modulos.anonimizacion.dominio.fabricas import FabricaAnonimizacion
from seguridad.modulos.anonimizacion.infraestructura.fabricas import FabricaRepositorio
from seguridad.modulos.anonimizacion.infraestructura.repositorios import Repositorioanonimizacion
from .mapeadores import MapeadorAnonimizacion

from .dto import AnonimizacionDTO

class ServicioAnonimizacion(Servicio):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_anonimizacion: FabricaAnonimizacion = FabricaAnonimizacion()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_anonimizacion(self):
        return self._fabrica_anonimizacion

    def crear_anonimizacion(self, anonimizacion_dto: AnonimizacionDTO) -> AnonimizacionDTO:
        anonimizacion: Anonimizacion = self.fabrica_anonimizacion.crear_objeto(anonimizacion_dto, MapeadorAnonimizacion())
        repositorio = self.fabrica_repositorio.crear_objeto(Repositorioanonimizacion.__class__)
        repositorio.agregar(anonimizacion)
        return self.fabrica_anonimizacion.crear_objeto(anonimizacion, MapeadorAnonimizacion())

    def obtener_anonimizacion_por_id(self, id) -> AnonimizacionDTO:
        repositorio = self.fabrica_repositorio.crear_objeto(Repositorioanonimizacion.__class__)
        return repositorio.obtener_por_id(id).__dict__
    
    def obtener_todas_las_anonimizacion(self) -> list[AnonimizacionDTO]:
        repositorio = self.fabrica_repositorio.crear_objeto(Repositorioanonimizacion.__class__)
        anonimizacion = repositorio.obtener_todos()
        mapeador = MapeadorAnonimizacion()
        anonimizacion_dto = [mapeador.entidad_a_dto(anonimizacion) for anonimizacion in anonimizacion]
        return anonimizacion_dto
    