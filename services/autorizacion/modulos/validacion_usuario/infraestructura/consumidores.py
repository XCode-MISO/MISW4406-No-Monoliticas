import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import json
from datetime import datetime

from autorizacion.modulos.validacion_usuario.infraestructura.schema.v1.eventos import Validacion_UsuarioFinalizada, ErrorValidacion_Usuario

from autorizacion.modulos.validacion_usuario.infraestructura.schema.v1.comandos import ComandoCrearValidacion_Usuario, ComandoErrorValidacion_Usuario
from autorizacion.seedwork.infraestructura import utils

from autorizacion.modulos.validacion_usuario.aplicacion.mapeadores import MapeadorValidacion_UsuarioDTOJson
from autorizacion.modulos.validacion_usuario.aplicacion.servicios import ServicioValidacion_Usuario

from autorizacion.modulos.validacion_usuario.infraestructura.despachadores import Despachador

def suscribirse_a_eventos():
    cliente = None
    topico = 'public/default/evento-validacion-usuario-finalizada'
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe(topico, consumer_type=_pulsar.ConsumerType.Shared,subscription_name='autorizacion-sub-eventos', schema=AvroSchema(Validacion_UsuarioFinalizada))

        print("\n================> suscribirse_a_eventos()")
        while True:
            mensaje = consumidor.receive()
            print(f'\n================> Evento recibido: {mensaje.value()}')
            try:
                consumidor.acknowledge(mensaje)
            except:
                pass 
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_eventos_error():
    topico = 'public/default/evento-error-validacion-usuario'
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe(topico, consumer_type=_pulsar.ConsumerType.Shared,subscription_name='autorizacion-sub-eventos', schema=AvroSchema(ErrorValidacion_Usuario))

        print("\n================> suscribirse_a_eventos_error()")
        while True:
            mensaje = consumidor.receive()
            print(f'\n========suscribirse_a_eventos_error()========> Evento recibido: {mensaje.value()}')
            try:
                comando = ErrorValidacion_Usuario("maligno")
                despachador = Despachador()
                despachador.publicar_comando_error(comando, 'public/default/comandos-error_usuario')
                consumidor.acknowledge(mensaje)
            except:
                pass 
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos de error!')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_comandos():    
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('public/default/comandos-validacion_usuario', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='autorizacion-sub-comandos', schema=AvroSchema(ComandoCrearValidacion_Usuario))
        print("\n================> suscribirse_a_comandos()")
        while True:
            mensaje = consumidor.receive()
            print(f'\n========suscribirse_a_comandos========> Comando recibido: {mensaje.value().data}')
            validacion_usuario_dict = mensaje.value().data.__dict__
            login_usuario = validacion_usuario_dict["id"]
            if(login_usuario == "maligno"):
                despacharEventoErrorUsuario(login_usuario)
            else:
                map_validacion_usuario = MapeadorValidacion_UsuarioDTOJson()
                validacion_usuario_dto = map_validacion_usuario.externo_a_dto(validacion_usuario_dict)
                sr = ServicioValidacion_Usuario()
                dto_final = sr.crear_validacion_usuario(validacion_usuario_dto)
                despacharEventoUsuarioValido(validacion_usuario_dto)
            consumidor.acknowledge(mensaje)
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_comandos_error():    
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('public/default/comandos-error_usuario', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='autorizacion-sub-comandos', schema=AvroSchema(ComandoErrorValidacion_Usuario))
        print("\n================> suscribirse_a_comandos_error()")
        while True:
            mensaje = consumidor.receive()
            print(f'\n========suscribirse_a_comandos_error========> Comando recibido: {mensaje.value().data}')
            sr = ServicioValidacion_Usuario()
            sr.borrar_usuario_maligno(mensaje.value().data)
            consumidor.acknowledge(mensaje)
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos de error!')
        traceback.print_exc()
        if cliente:
            cliente.close()

def despacharEventoErrorUsuario(login_usuario):
    print(f"\n================> Usuario maligno detectado:", login_usuario)
    evento = ErrorValidacion_Usuario(
        nombre = login_usuario
    )
    print(f"\n================> evento: ", evento)
    despachador = Despachador()
    despachador.pub_mensaje_error(evento, 'public/default/evento-error-validacion-usuario')
    print("\n=================> Evento despachado!!!!!!!!!")    

def despacharEventoUsuarioValido(validacion_usuario_dto):
    print("\n=================> parametro dto: ", validacion_usuario_dto)
    evento = Validacion_UsuarioFinalizada(
        id = "1232321321",
        id_correlacion = "389822434",
        ingestion_id = "6463454",
        imagen = "https://upload.wikimedia.org/wikipedia/commons/3/32/Dark_Brandon.jpg",
        nombre = "dark-brandon",
        fecha_creacion = "2025-03-02T22:48:08Z"
    )
    print(f"\n=================> evento: ", evento)
    despachador = Despachador()
    despachador.pub_mensaje(evento, 'public/default/evento-validacion-usuario-finalizada')
    print("\n=================> Evento despachado!!!!!!!!!")    