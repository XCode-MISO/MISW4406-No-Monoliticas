from seguridad.seedwork.aplicacion.comandos import ComandoHandler
from seguridad.modulos.hippa.infraestructura.fabricas import FabricaRepositorio
from seguridad.modulos.hippa.dominio.fabricas import FabricaValidacionHippa 

class CrearValidacionHippaBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_validacion_hippa = FabricaValidacionHippa()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_validacion_hippa(self):
        return self._fabrica_validacion_hippa    
    