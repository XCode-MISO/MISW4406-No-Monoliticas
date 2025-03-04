""" Interfaces para los repositorios del dominio de vuelos

En este archivo usted encontrará las diferentes interfaces para repositorios
del dominio de vuelos

"""

from abc import ABC
from autorizacion.seedwork.dominio.repositorios import Repositorio

class RepositorioValidacion_Usuario(Repositorio, ABC):
    ...

class RepositorioUsuario(Repositorio, ABC):
    ...
