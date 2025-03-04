""" Excepciones del dominio de vuelos

En este archivo usted encontrará los Excepciones relacionadas
al dominio de vuelos

"""
from autorizacion.seedwork.dominio.excepciones import ExcepcionFabrica

class TipoObjetoNoExisteEnDominiovalidacion_usuarioExcepcion(ExcepcionFabrica):
    def __init__(self, mensaje='No existe una fábrica para el tipo solicitado en el módulo de validacion_usuario'):
        self.__mensaje = mensaje
    def __str__(self):
        return str(self.__mensaje)