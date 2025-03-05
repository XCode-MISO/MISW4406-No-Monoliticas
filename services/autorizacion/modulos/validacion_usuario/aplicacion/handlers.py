from autorizacion.modulos.validacion_usuario.dominio.eventos import Validacion_UsuarioAgregada
from autorizacion.seedwork.aplicacion.handlers import Handler
from autorizacion.modulos.validacion_usuario.infraestructura.despachadores import Despachador

class HandlerReservaIntegracion(Handler):
    @staticmethod
    def handle_validacion_usuario_creada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'public/default/eventos-validacion_usuario')

    @staticmethod
    def handle_validacion_usuario_agregada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'public/default/eventos-validacion_usuario')

    @staticmethod
    def handle_validacion_usuario_iniciada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'public/default/eventos-validacion_usuario')

    @staticmethod
    def handle_validacion_usuario_cancelada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'public/default/eventos-validacion_usuario')

    @staticmethod
    def handle_validacion_usuario_finalizada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'public/default/eventos-validacion_usuario')
