from seguridad.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from seguridad.seedwork.aplicacion.queries import ejecutar_query as query
from seguridad.modulos.anonimizacion.infraestructura.repositorios import RepositorioAnonimizaciones
from dataclasses import dataclass
from .base import AnonimizacionQueryBaseHandler
from seguridad.modulos.anonimizacion.aplicacion.mapeadores import MapeadorAnonimizacion
import uuid

@dataclass
class ObtenerAnonimizacion(Query):
    id: str

class ObtenerReservaHandler(AnonimizacionQueryBaseHandler):

    def handle(self, query: ObtenerAnonimizacion) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioAnonimizaciones.__class__)
        anonimizacion =  self.fabrica_anonimizacion.crear_objeto(repositorio.obtener_por_id(query.id), MapeadorAnonimizacion())
        return QueryResultado(resultado=anonimizacion)

@query.register(ObtenerAnonimizacion)
def ejecutar_query_obtener_anonimizacion(query: ObtenerAnonimizacion):
    handler = ObtenerReservaHandler()
    return handler.handle(query)