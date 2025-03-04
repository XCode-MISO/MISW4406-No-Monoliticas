""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de vuelos

"""

from dataclasses import dataclass, field
from autorizacion.seedwork.dominio.fabricas import Fabrica
from autorizacion.seedwork.dominio.repositorios import Repositorio
from autorizacion.modulos.validacion_usuario.dominio.repositorios import RepositorioValidacion_Usuario
from .repositorios import RepositorioValidacion_UsuarioMYSQL
from .excepciones import ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioValidacion_Usuario.__class__:
            return RepositorioValidacion_UsuarioMYSQL()
        else:
            raise ExcepcionFabrica()