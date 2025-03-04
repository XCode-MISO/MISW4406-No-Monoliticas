""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de vuelos

"""

from autorizacion.config.db import db
from autorizacion.modulos.envio_imagen.dominio.repositorios import RepositorioValidacionesEnvio_Imagen
from autorizacion.modulos.envio_imagen.dominio.entidades import ValidacionEnvio_Imagen
from autorizacion.modulos.envio_imagen.dominio.fabricas import FabricaValidacionEnvio_Imagen
from .dto import ValidacionEnvio_Imagen as ValidacionEnvio_ImagenDTO
from .mapeadores import MapeadorValidacionEnvio_Imagen
from uuid import UUID

import logging

class RepositorioValidacion_UsuarioMYSQL(RepositorioValidacionesEnvio_Imagen):

    def __init__(self):
        self._fabrica_validaciones_envio_imagen: FabricaValidacionEnvio_Imagen = FabricaValidacionEnvio_Imagen()

    @property
    def fabrica_validaciones_envio_imagen(self):
        return self._fabrica_validaciones_envio_imagen

    def obtener_por_id(self, id: UUID) -> ValidacionEnvio_Imagen:
        validacion_envio_imagen_dto = db.session.query(ValidacionEnvio_ImagenDTO).filter_by(id=str(id)).one()
        return self.fabrica_validaciones_envio_imagen.crear_objeto(validacion_envio_imagen_dto, MapeadorValidacionEnvio_Imagen())

    def obtener_todos(self) -> list[ValidacionEnvio_Imagen]:
        # TODO
        raise NotImplementedError

    def agregar(self, validacion_envio_imagen: ValidacionEnvio_Imagen):
        validacion_envio_imagen_dto = self.fabrica_validaciones_envio_imagen.crear_objeto(validacion_envio_imagen, MapeadorValidacionEnvio_Imagen())
        db.session.add(validacion_envio_imagen_dto)
        db.session.commit()

    def actualizar(self, validacion_envio_imagen: ValidacionEnvio_Imagen):
        # TODO
        raise NotImplementedError

    def eliminar(self, validacion_envio_imagen_id: UUID):
        # TODO
        raise NotImplementedError