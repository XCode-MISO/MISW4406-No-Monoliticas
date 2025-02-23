from seguridad.seedwork.aplicacion.comandos import ComandoHandler
from seguridad.modulos.anonimizacion.infraestructura.fabricas import FabricaRepositorio
from seguridad.modulos.anonimizacion.dominio.fabricas import FabricaAnonimizacion 

class CrearAnonimizacionBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_anonimizacion = FabricaAnonimizacion()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_anonimizacion(self):
        return self._fabrica_anonimizacion    
    