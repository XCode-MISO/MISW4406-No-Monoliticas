""" Fábricas para la creación de objetos del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de vuelos

"""

from .entidades import Reserva
from .reglas import MinimoUnItinerario, RutaValida
from .excepciones import TipoObjetoNoExisteEnDominioVuelosExcepcion
from seguridad.seedwork.dominio.repositorios import Mapeador, Repositorio
from seguridad.seedwork.dominio.fabricas import Fabrica
from seguridad.seedwork.dominio.entidades import Entidad
from seguridad.modulos.anonimizacion.dominio.entidades import Anonimizacion
from dataclasses import dataclass

@dataclass
class FabricaAnonimizacion(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            anonimizacion: Anonimizacion = mapeador.dto_a_entidad(obj)
            return anonimizacion
