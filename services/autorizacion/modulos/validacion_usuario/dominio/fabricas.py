""" Fábricas para la creación de objetos del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de vuelos

"""

from .entidades import Validacion_Usuario, Usuario
from autorizacion.seedwork.dominio.repositorios import Mapeador, Repositorio
from autorizacion.seedwork.dominio.fabricas import Fabrica
from autorizacion.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass

@dataclass
class _FabricaValidacion_Usuario(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)            
        else:
            validacion_usuario: Validacion_Usuario = mapeador.dto_a_entidad(obj)
            print(validacion_usuario)
            return validacion_usuario

@dataclass
class FabricaValidacion_Usuario(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        fabrica_reserva = _FabricaValidacion_Usuario()
        return fabrica_reserva.crear_objeto(obj, mapeador)
    
    
@dataclass
class _FabricaUsuario(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)            
        else:
            usuario: Usuario = mapeador.dto_a_entidad(obj)
            print(usuario)
            return usuario

@dataclass
class FabricaUsuario(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        fabrica_reserva = _FabricaUsuario()
        return fabrica_reserva.crear_objeto(obj, mapeador)