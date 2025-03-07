from seguridad.modulos.anonimizacion.dominio.eventos import AnonimizacionAgregada
from seguridad.seedwork.aplicacion.handlers import Handler
from seguridad.modulos.anonimizacion.infraestructura.despachadores import Despachador

class HandlerReservaIntegracion(Handler):
    @staticmethod
    def handle_anonimizacion_creada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'public/default/eventos-anonimizacion')

    @staticmethod
    def handle_anonimizacion_agregada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'public/default/eventos-anonimizacion-finalizada')

    @staticmethod
    def handle_anonimizacion_iniciada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'public/default/eventos-anonimizacion')

    @staticmethod
    def handle_anonimizacion_cancelada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'public/default/eventos-anonimizacion')

    @staticmethod
    def handle_anonimizacion_finalizada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'public/default/eventos-anonimizacion')
