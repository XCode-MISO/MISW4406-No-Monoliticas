from seguridad.seedwork.aplicacion.comandos import Comando
from seguridad.modulos.anonimizacion.aplicacion.dto import AnonimizacionDTO
from .base import CrearAnonimizacionBaseHandler
from dataclasses import dataclass, field
from seguridad.seedwork.aplicacion.comandos import ejecutar_commando as comando

from seguridad.modulos.anonimizacion.dominio.entidades import Anonimizacion
from seguridad.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from seguridad.modulos.anonimizacion.aplicacion.mapeadores import MapeadorAnonimizacion
from seguridad.modulos.anonimizacion.infraestructura.repositorios import Repositorioanonimizacion

@dataclass
class CrearAnonimizacion(Comando):
    fecha_creacion: str
    fecha_actualizacion: str
    id: str
    nombre: str
    imagen: str
    fecha_fin: str
    


class CrearAnonimizacionHandler(CrearAnonimizacionBaseHandler):
    
    def handle(self, comando: CrearAnonimizacion):
        anonimizacion_dto = AnonimizacionDTO(
                fecha_actualizacion=comando.fecha_actualizacion
            ,   fecha_creacion=comando.fecha_creacion
            ,   id=comando.id
            ,   nombre=comando.id
            ,   imagen=comando.id
            ,   fecha_fin=comando.id
            )

        anonimizacion: Anonimizacion = self.fabrica_anonimizacion.crear_objeto(anonimizacion_dto, MapeadorAnonimizacion())
        anonimizacion.crear_anonimizacion(anonimizacion)

        repositorio = self.fabrica_repositorio.crear_objeto(Repositorioanonimizacion.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, anonimizacion)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(CrearAnonimizacion)
def ejecutar_comando_crear_anonimizacion(comando: CrearAnonimizacion):
    print(f'Ejecutandoc comando crear anonimizacion desde el handler: {comando.__class__}')
    handler = CrearAnonimizacionHandler()
    handler.handle(comando)