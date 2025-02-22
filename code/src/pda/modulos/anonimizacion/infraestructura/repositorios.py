""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de vuelos

"""

from pda.config.db import db
from pda.modulos.anonimizacion.dominio.repositorios import RepositorioAnonimizaciones
from pda.modulos.anonimizacion.dominio.objetos_valor import NombreAero, Odo, Leg, Segmento, Itinerario, CodigoIATA
from pda.modulos.anonimizacion.dominio.entidades import Proveedor, Aeropuerto, Reserva
from pda.modulos.anonimizacion.dominio.fabricas import FabricaAnonimizacion
from .dto import Reserva as ReservaDTO
from .mapeadores import MapeadorReserva
from uuid import UUID

class RepositorioAnonimizacionesMYSQL(RepositorioAnonimizaciones):

    def __init__(self):
        self._fabrica_anonimizaciones: FabricaAnonimizacion = FabricaAnonimizacion()

    @property
    def fabrica_anonimizaciones(self):
        return self._fabrica_anonimizaciones

    def obtener_por_id(self, id: UUID) -> Anonimizacion:
        reserva_dto = db.session.query(AnonimizacionDTO).filter_by(id=str(id)).one()
        return self.fabrica_anonimizaciones.crear_objeto(reserva_dto, MapeadorAnonimizacion())

    def obtener_todos(self) -> list[Anonimizacion]:
        # TODO
        raise NotImplementedError

    def agregar(self, reserva: Anonimizacion):
        reserva_dto = self.fabrica_anonimizaciones.crear_objeto(reserva, MapeadorAnonimizacion())
        db.session.add(reserva_dto)

    def actualizar(self, reserva: Anonimizacion):
        # TODO
        raise NotImplementedError

    def eliminar(self, reserva_id: UUID):
        # TODO
        raise NotImplementedError