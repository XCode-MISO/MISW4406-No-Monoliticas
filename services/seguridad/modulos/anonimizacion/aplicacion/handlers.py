from seguridad.modulos.anonimizacion.dominio.eventos import AnonimizacionAgregada
from seguridad.seedwork.aplicacion.handlers import Handler
from seguridad.modulos.anonimizacion.infraestructura.despachadores import Despachador

class HandlerReservaIntegracion(Handler):

    @staticmethod
    def handle_anonimizacion_agregada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-anonimizacion')
