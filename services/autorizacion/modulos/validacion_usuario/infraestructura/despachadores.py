import pulsar
from pulsar.schema import *

from autorizacion.modulos.validacion_usuario.infraestructura.schema.v1.eventos import Validacion_UsuarioAgregada, Validacion_UsuarioAgregadaPayload
from autorizacion.modulos.validacion_usuario.infraestructura.schema.v1.eventos import Validacion_UsuarioFinalizada, ErrorValidacion_Usuario
from autorizacion.modulos.validacion_usuario.infraestructura.schema.v1.comandos import ComandoCrearValidacion_Usuario, ComandoCrearValidacion_UsuarioPayload
from autorizacion.modulos.validacion_usuario.infraestructura.schema.v1.comandos import ComandoErrorValidacion_Usuario, ComandoErrorValidacion_UsuarioPayload
from autorizacion.seedwork.infraestructura import utils

import datetime

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

class Despachador:
    def pub_mensaje(self, mensaje, topico):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(Validacion_UsuarioFinalizada))
        publicador.send(mensaje)
        cliente.close()

    def pub_mensaje_error(self, mensaje, topico):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(ErrorValidacion_Usuario))
        publicador.send(mensaje)
        cliente.close()

    def pub_mensaje_x(self, mensaje, topico):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(mensaje.__class__))
        publicador.send(mensaje)
        cliente.close()

    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(Validacion_UsuarioAgregada))
        publicador.send(mensaje)
        cliente.close()
    
    def _publicar_mensaje_comando(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(ComandoCrearValidacion_Usuario))
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento, topico):
        payload = Validacion_UsuarioAgregadaPayload(
            id_validacion_usuario=str(evento.id_reserva), 
            estado=str(evento.estado), 
            fecha_validacion=int(unix_time_millis(evento.fecha_validacion))
        )
        evento_integracion = Validacion_UsuarioAgregada(data=payload)
        self._publicar_mensaje(evento_integracion, topico, AvroSchema(Validacion_UsuarioAgregada))

    def publicar_comando(self, comando, topico):
        payload = ComandoCrearValidacion_UsuarioPayload(
            fecha_actualizacion = comando.fecha_actualizacion,
            fecha_validacion  = comando.fecha_validacion,
            id = comando.id,
            usuario= comando.usuario,
            nombre = comando.nombre,
            imagen = comando.imagen,
            fecha_fin = comando.fecha_fin
        )
        comando_integracion = ComandoCrearValidacion_Usuario(data=payload)
        self._publicar_mensaje_comando(comando_integracion, topico, AvroSchema(ComandoCrearValidacion_Usuario))

################################################################
    def _publicar_mensaje_comando_error(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(ComandoErrorValidacion_Usuario))
        publicador.send(mensaje)
        cliente.close()

    def publicar_comando_error(self, comando, topico):
        payload = ComandoErrorValidacion_UsuarioPayload(
            nombre = comando.nombre
        )
        comando_integracion = ComandoErrorValidacion_Usuario(data=payload)
        self._publicar_mensaje_comando_error(comando_integracion, topico, AvroSchema(ComandoErrorValidacion_Usuario))
################################################################
