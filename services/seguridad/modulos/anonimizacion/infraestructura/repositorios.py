""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de vuelos

"""
from seguridad.config.db import db
from seguridad.modulos.anonimizacion.dominio.repositorios import Repositorioanonimizacion
from seguridad.modulos.anonimizacion.dominio.entidades import Anonimizacion
from seguridad.modulos.anonimizacion.dominio.fabricas import FabricaAnonimizacion
from .dto import Anonimizacion as AnonimizacionDTO
from .mapeadores import MapeadorAnonimizacion
from uuid import UUID

class RepositorioanonimizacionMYSQL(Repositorioanonimizacion):

    def __init__(self):
        self._fabrica_anonimizacion: FabricaAnonimizacion = FabricaAnonimizacion()

    @property
    def fabrica_anonimizacion(self):
        return self._fabrica_anonimizacion

    def obtener_por_id(self, id: UUID) -> Anonimizacion:
        anonimizacion_dto = db.session.query(AnonimizacionDTO).filter_by(id=str(id)).first()
        return self.fabrica_anonimizacion.crear_objeto(anonimizacion_dto, MapeadorAnonimizacion())

    def obtener_todos(self) -> list[Anonimizacion]:
        anonimizacion_dto = db.session.query(AnonimizacionDTO).all()
        anonimizacion: list[AnonimizacionDTO]=list()
            
        for anonimizacion in anonimizacion_dto:    
            anonimizacion.append(self.fabrica_anonimizacion.crear_objeto(anonimizacion, MapeadorAnonimizacion()))

        return anonimizacion
    
    def agregar(self, anonimizacion: Anonimizacion):
        try:
            anonimizacion_dto = self.fabrica_anonimizacion.crear_objeto(anonimizacion, MapeadorAnonimizacion())
            db.session.add(anonimizacion_dto)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print('Error al agregar la anonimizacion:', e)

    def actualizar(self, reserva: Anonimizacion):
        # TODO
        raise NotImplementedError

    def eliminar(self, reserva_id: UUID):
        # TODO
        raise NotImplementedError