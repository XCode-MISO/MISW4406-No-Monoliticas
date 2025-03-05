from autorizacion.modulos.envio_imagen.dominio.eventos import ValidacionEnvio_ImagenCancelada, ValidacionEnvio_ImagenCreada, ValidacionEnvio_ImagenFinalizada, ValidacionEnvio_ImagenIniciada
from autorizacion.seedwork.aplicacion.handlers import Handler
from autorizacion.modulos.envio_imagen.infraestructura.despachadores import Despachador

class HandlerEnvio_ImagenIntegracion(Handler):
    @staticmethod
    def handle_envio_imagen_creada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'public/default/eventos-envio_imagen')

    @staticmethod
    def handle_envio_imagen_agregada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'public/default/eventos-envio_imagen')

    @staticmethod
    def handle_envio_imagen_iniciada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'public/default/eventos-envio_imagen')

    @staticmethod
    def handle_envio_imagen_cancelada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'public/default/eventos-envio_imagen')

    @staticmethod
    def handle_envio_imagen_finalizada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'public/default/eventos-envio_imagen')
