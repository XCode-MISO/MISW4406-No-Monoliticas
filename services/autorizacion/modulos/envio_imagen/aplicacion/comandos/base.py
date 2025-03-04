from autorizacion.seedwork.aplicacion.comandos import ComandoHandler
from autorizacion.modulos.envio_imagen.infraestructura.fabricas import FabricaRepositorio
from autorizacion.modulos.envio_imagen.dominio.fabricas import FabricaValidacionEnvio_Imagen 

class CrearValidacionEnvio_ImagenBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_validacion_envio_imagen = FabricaValidacionEnvio_Imagen()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_validacion_envio_imagen(self):
        return self._fabrica_validacion_envio_imagen    
    