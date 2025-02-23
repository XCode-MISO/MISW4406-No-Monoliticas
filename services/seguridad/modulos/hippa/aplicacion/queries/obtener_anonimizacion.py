from seguridad.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from seguridad.seedwork.aplicacion.queries import ejecutar_query as query
from seguridad.modulos.hippa.infraestructura.repositorios import RepositorioValidacionesHippa
from dataclasses import dataclass
from .base import ValidacionHippaQueryBaseHandler
from seguridad.modulos.hippa.aplicacion.mapeadores import MapeadorAnonimizacion
import uuid

@dataclass
class ObtenerValidacionHippa(Query):
    id: str

class ObtenerReservaHandler(ValidacionHippaQueryBaseHandler):

    def handle(self, query: ObtenerValidacionHippa) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioValidacionesHippa.__class__)
        validacion_hippa =  self.fabrica_validacion_hippa.crear_objeto(repositorio.obtener_por_id(query.id), MapeadorAnonimizacion())
        return QueryResultado(resultado=validacion_hippa)

@query.register(ObtenerValidacionHippa)
def ejecutar_query_obtener_validacion_hippa(query: ObtenerValidacionHippa):
    handler = ObtenerReservaHandler()
    return handler.handle(query)