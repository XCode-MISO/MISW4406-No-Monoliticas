from aeroalpes.modulos.vuelos.dominio.eventos import anonimizacionCreada, ReservaCancelada, ReservaAprobada, ReservaPagada
from aeroalpes.seedwork.aplicacion.handlers import Handler
from aeroalpes.modulos.vuelos.infraestructura.despachadores import Despachador

class HandlerAnonimizacionIntegracion(Handler):
    @staticmethod
    def handle_anonimizacion_iniciada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-anonimizacion')

    @staticmethod
    def handle_anonimizacion_cancelada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-anonimizacion')

    @staticmethod
    def handle_anonimizacion_finalizada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-anonimizacion')
