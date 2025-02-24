from seguridad.seedwork.aplicacion.comandos import Comando
from seguridad.modulos.hippa.aplicacion.dto import ImagenHippaDTO
from .base import CrearValidacionHippaBaseHandler
from dataclasses import dataclass, field
from seguridad.seedwork.aplicacion.comandos import ejecutar_commando as comando

from seguridad.modulos.hippa.dominio.entidades import ValidacionHippa
from seguridad.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from seguridad.modulos.hippa.aplicacion.mapeadores import MapeadorValidacionHippa
from seguridad.modulos.hippa.infraestructura.repositorios import RepositorioValidacionesHippa

import logging
logger = logging.getLogger(__name__)

@dataclass
class CrearValidacionHippa(Comando):
    id: str
    image: str
    estado:str
    fecha_creacion: str
    fecha_actualizacion: str

class CrearValidacionHippaHandler(CrearValidacionHippaBaseHandler):
    def handle(self, comando: CrearValidacionHippa):
        validacion_hippa_dto = ImagenHippaDTO(
                fecha_actualizacion=comando.fecha_actualizacion
            ,   fecha_creacion=comando.fecha_creacion
            ,   id=comando.id
            ,   imagen=comando.image)
        logger.debug("antes de llamar el repositorio"+validacion_hippa)

        validacion_hippa: ValidacionHippa = self.fabrica_repositorio.crear_objeto(validacion_hippa_dto, MapeadorValidacionHippa())
        validacion_hippa.crear_anonimizacion(validacion_hippa)
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioValidacionesHippa.__class__)

        logger.debug("antes hacer el unit of work"+validacion_hippa)
        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, validacion_hippa)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()

@comando.register(CrearValidacionHippa)
def ejecutar_comando_crear_validacion_hippa(comando: CrearValidacionHippa):
    handler = CrearValidacionHippaHandler()
    handler.handle(comando)
    