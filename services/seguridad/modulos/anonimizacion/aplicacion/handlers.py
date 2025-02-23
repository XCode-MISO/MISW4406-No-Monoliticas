from seguridad.modulos.anonimizacion.dominio.eventos import AnonimizacionCancelada, AnonimizacionCreada, AnonimizacionFinalizada, AnonimizacionIniciada
from seguridad.seedwork.aplicacion.handlers import Handler
from seguridad.modulos.anonimizacion.infraestructura.despachadores import Despachador

class HandlerAnonimizacionIntegracion(Handler):
    @staticmethod
    def handle_anonimizacion_creada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-anonimizacion')

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
