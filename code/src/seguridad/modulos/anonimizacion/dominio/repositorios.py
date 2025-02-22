""" Interfaces para los repositorios del dominio de vuelos

En este archivo usted encontrará las diferentes interfaces para repositorios
del dominio de vuelos

"""

from abc import ABC
from seguridad.seedwork.dominio.repositorios import Repositorio

class RepositorioAnonimizaciones(Repositorio, ABC):
    ...