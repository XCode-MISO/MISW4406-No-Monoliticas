""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de vuelos

"""

from dataclasses import dataclass, field
from seguridad.seedwork.dominio.fabricas import Fabrica
from seguridad.seedwork.dominio.repositorios import Repositorio
from seguridad.modulos.anonimizacion.dominio.repositorios import Repositorioanonimizacion
from .repositorios import RepositorioanonimizacionSQLite
from .excepciones import ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == Repositorioanonimizacion.__class__:
            return RepositorioanonimizacionSQLite()
        else:
            raise ExcepcionFabrica()