from autorizacion.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from autorizacion.seedwork.aplicacion.queries import ejecutar_query as query
from autorizacion.modulos.envio_imagen.infraestructura.repositorios import RepositorioValidacionesEnvio_Imagen
from dataclasses import dataclass
from .base import ValidacionEnvio_ImagenQueryBaseHandler
from autorizacion.modulos.envio_imagen.aplicacion.mapeadores import MapeadorValidacionEnvio_Imagen
import uuid

@dataclass
class ObtenerValidacionEnvio_Imagen(Query):
    id: str

class ObtenerValidacionEnvio_ImagenHandler(ValidacionEnvio_ImagenQueryBaseHandler):

    def handle(self, query: ObtenerValidacionEnvio_Imagen) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioValidacionesEnvio_Imagen.__class__)
        validacion_envio_imagen =  self.fabrica_validacion_envio_imagen.crear_objeto(repositorio.obtener_por_id(query.id), MapeadorValidacionEnvio_Imagen())
        return QueryResultado(resultado=validacion_envio_imagen)

@query.register(ObtenerValidacionEnvio_Imagen)
def ejecutar_query_obtener_validacion_envio_imagen(query: ObtenerValidacionEnvio_Imagen):
    handler = ObtenerValidacionEnvio_ImagenHandler()
    return handler.handle(query)