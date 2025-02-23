from seguridad.modulos.hippa.dominio.eventos import ValidacionHippaCancelada, ValidacionHippaCreada, ValidacionHippaFinalizada, ValidacionHippaIniciada
from seguridad.seedwork.aplicacion.handlers import Handler
from seguridad.modulos.hippa.infraestructura.despachadores import Despachador

class HandlerHippaIntegracion(Handler):
    @staticmethod
    def handle_hippa_creada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-hippa')

    @staticmethod
    def handle_hippa_iniciada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-hippa')

    @staticmethod
    def handle_hippa_cancelada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-hippa')

    @staticmethod
    def handle_hippa_finalizada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-hippa')
