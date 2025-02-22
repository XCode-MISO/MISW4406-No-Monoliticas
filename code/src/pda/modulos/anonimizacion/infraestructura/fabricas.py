""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de vuelos

"""

from dataclasses import dataclass, field
from pda.seedwork.dominio.fabricas import Fabrica
from pda.seedwork.dominio.repositorios import Repositorio
from pda.modulos.anonimizacion.dominio.repositorios import RepositorioAnonimizaciones
from .repositorios import RepositorioAnonimizacionesMYSQL
from .excepciones import ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioAnonimizaciones.__class__:
            return RepositorioAnonimizacionesMYSQL()
        else:
            raise ExcepcionFabrica()