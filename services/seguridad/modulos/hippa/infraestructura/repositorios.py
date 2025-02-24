""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de vuelos

"""

from seguridad.config.db import db
from seguridad.modulos.hippa.dominio.repositorios import RepositorioValidacionesHippa
from seguridad.modulos.hippa.dominio.entidades import ValidacionHippa
from seguridad.modulos.hippa.dominio.fabricas import FabricaValidacionHippa
from .dto import ValidacionHippa as ValidacionHippaDTO
from .mapeadores import MapeadorValidacionHippa
from uuid import UUID

import logging

class RepositorioanonimizacionSQLite(RepositorioValidacionesHippa):

    def __init__(self):
        self._fabrica_validaciones_hippa: FabricaValidacionHippa = FabricaValidacionHippa()

    @property
    def fabrica_validaciones_hippa(self):
        return self._fabrica_validaciones_hippa

    def obtener_por_id(self, id: UUID) -> ValidacionHippa:
        validacion_hippa_dto = db.session.query(ValidacionHippaDTO).filter_by(id=str(id)).one()
        return self.fabrica_validaciones_hippa.crear_objeto(validacion_hippa_dto, MapeadorValidacionHippa())

    def obtener_todos(self) -> list[ValidacionHippa]:
        # TODO
        raise NotImplementedError

    def agregar(self, validacion_hippa: ValidacionHippa):
        validacion_hippa_dto = self.fabrica_validaciones_hippa.crear_objeto(validacion_hippa, MapeadorValidacionHippa())
        db.session.add(validacion_hippa_dto)
        db.session.commit()

    def actualizar(self, validacion_hippa: ValidacionHippa):
        # TODO
        raise NotImplementedError

    def eliminar(self, validacion_hippa_id: UUID):
        # TODO
        raise NotImplementedError