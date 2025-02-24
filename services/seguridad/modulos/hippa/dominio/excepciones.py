""" Excepciones del dominio de vuelos

En este archivo usted encontrará los Excepciones relacionadas
al dominio de vuelos

"""
from seguridad.seedwork.dominio.excepciones import ExcepcionFabrica

class TipoObjetoNoExisteEnDominioanonimizacionExcepcion(ExcepcionFabrica):
    def __init__(self, mensaje='No existe una fábrica para el tipo solicitado en el módulo de anonimizacion'):
        self.__mensaje = mensaje
    def __str__(self):
        return str(self.__mensaje)