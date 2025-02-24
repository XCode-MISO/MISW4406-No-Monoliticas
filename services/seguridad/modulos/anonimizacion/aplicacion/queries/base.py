from seguridad.seedwork.aplicacion.queries import QueryHandler
from seguridad.modulos.anonimizacion.infraestructura.fabricas import FabricaRepositorio
from seguridad.modulos.anonimizacion.dominio.fabricas import FabricaAnonimizacion

class ReservaQueryBaseHandler(QueryHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_anonimizacion: FabricaAnonimizacion = FabricaAnonimizacion()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_anonimizacion(self):
        return self._fabrica_anonimizacion   