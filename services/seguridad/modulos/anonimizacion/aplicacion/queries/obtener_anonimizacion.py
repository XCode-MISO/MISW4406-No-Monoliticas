from seguridad.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from seguridad.seedwork.aplicacion.queries import ejecutar_query as query
from seguridad.modulos.anonimizacion.infraestructura.repositorios import Repositorioanonimizacion
from dataclasses import dataclass
from .base import ReservaQueryBaseHandler
from seguridad.modulos.anonimizacion.aplicacion.mapeadores import MapeadorAnonimizacion
import uuid

@dataclass
class ObtenerAnonimizacion(Query):
    id: str

class ObtenerAnonimizacionHandler(ReservaQueryBaseHandler):

    def handle(self, query: ObtenerAnonimizacion) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(Repositorioanonimizacion.__class__)
        reserva =  self.fabrica_anonimizacion.crear_objeto(repositorio.obtener_por_id(query.id), MapeadorAnonimizacion())
        return QueryResultado(resultado=reserva)

@query.register(ObtenerAnonimizacion)
def ejecutar_query_obtener_reserva(query: ObtenerAnonimizacion):
    handler = ObtenerAnonimizacionHandler()
    return handler.handle(query)