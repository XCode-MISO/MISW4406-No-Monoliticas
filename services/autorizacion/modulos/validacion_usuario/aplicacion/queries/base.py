from autorizacion.seedwork.aplicacion.queries import QueryHandler
from autorizacion.modulos.validacion_usuario.infraestructura.fabricas import FabricaRepositorio
from autorizacion.modulos.validacion_usuario.dominio.fabricas import FabricaValidacion_Usuario

class ReservaQueryBaseHandler(QueryHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_validacion_usuario: FabricaValidacion_Usuario = FabricaValidacion_Usuario()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_validacion_usuario(self):
        return self._fabrica_validacion_usuario   