from seguridad.seedwork.aplicacion.comandos import Comando
from seguridad.modulos.anonimizacion.aplicacion.dto import AnonimizacionDTO
from dataclasses import dataclass, field
from seguridad.seedwork.aplicacion.comandos import ejecutar_commando as comando
from .base import CrearAnonimizacionBaseHandler

from seguridad.modulos.anonimizacion.dominio.entidades import Anonimizacion
from seguridad.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from seguridad.modulos.anonimizacion.aplicacion.mapeadores import MapeadorReserva
from seguridad.modulos.anonimizacion.infraestructura.repositorios import RepositorioReservas

@dataclass
class CrearAnonimizacion(Comando):
    fecha_creacion: str
    fecha_actualizacion: str
    id: str
    image: str


class CrearAnonimizacionHandler(CrearAnonimizacionBaseHandler):
    def handle(self, comando: CrearAnonimizacion):
        anonimizacion = AnonimizacionDTO(
                fecha_actualizacion=comando.fecha_actualizacion
            ,   fecha_creacion=comando.fecha_creacion
            ,   id=comando.id
            ,   itinerarios=comando.itinerarios)

        anonimizacion: Anonimizacion = self.fabrica_repositorio.crear_objeto(anonimizacion, MapeadorReserva())
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioReservas.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, anonimizacion)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()

@comando.register(CrearAnonimizacion)
def ejecutar_comando_crear_reserva(comando: CrearAnonimizacion):
    handler = CrearAnonimizacionHandler()
    handler.handle(comando)
    