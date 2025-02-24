""" Fábricas para la creación de objetos del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de vuelos

"""

from .entidades import Anonimizacion
from .excepciones import TipoObjetoNoExisteEnDominioanonimizacionExcepcion
from seguridad.seedwork.dominio.repositorios import Mapeador, Repositorio
from seguridad.seedwork.dominio.fabricas import Fabrica
from seguridad.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass

@dataclass
class _FabricaAnonimizacion(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)            
        else:
            anonimizacion: Anonimizacion = mapeador.dto_a_entidad(obj)
            print(anonimizacion)
            #self.validar_regla(TamanioMayorAMetro(anonimizacion))
            return anonimizacion

@dataclass
class FabricaAnonimizacion(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        fabrica_reserva = _FabricaAnonimizacion()
        return fabrica_reserva.crear_objeto(obj, mapeador)