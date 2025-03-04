from autorizacion.seedwork.aplicacion.comandos import Comando
from autorizacion.modulos.envio_imagen.aplicacion.dto import ImagenEnvio_ImagenDTO
from .base import CrearValidacionEnvio_ImagenBaseHandler
from dataclasses import dataclass, field
from autorizacion.seedwork.aplicacion.comandos import ejecutar_commando as comando

from autorizacion.modulos.envio_imagen.dominio.entidades import ValidacionEnvio_Imagen
from autorizacion.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from autorizacion.modulos.envio_imagen.aplicacion.mapeadores import MapeadorValidacionEnvio_Imagen
from autorizacion.modulos.envio_imagen.infraestructura.repositorios import RepositorioValidacionesEnvio_Imagen

import logging

@dataclass
class CrearValidacionEnvio_Imagen(Comando):
    id: str
    image: str
    fecha_validacion: str
    fecha_actualizacion: str
    estado: str

class CrearValidacionEnvio_ImagenHandler(CrearValidacionEnvio_ImagenBaseHandler):
    def handle(self, comando: CrearValidacionEnvio_Imagen):
        validacion_envio_imagen_dto = ImagenEnvio_ImagenDTO(
                fecha_actualizacion=comando.fecha_actualizacion
            ,   fecha_validacion=comando.fecha_validacion
            ,   id=comando.id
            ,   imagen=comando.image
            ,   estado=comando.estado)

        validacion_envio_imagen: ValidacionEnvio_Imagen = self.fabrica_repositorio.crear_objeto(validacion_envio_imagen_dto, MapeadorValidacionEnvio_Imagen())
        validacion_envio_imagen.crear_validacion_usuario(validacion_envio_imagen)
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioValidacionesEnvio_Imagen.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, validacion_envio_imagen)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()

@comando.register(CrearValidacionEnvio_Imagen)
def ejecutar_comando_crear_validacion_envio_imagen(comando: CrearValidacionEnvio_Imagen):
    handler = CrearValidacionEnvio_ImagenHandler()
    handler.handle(comando)
    