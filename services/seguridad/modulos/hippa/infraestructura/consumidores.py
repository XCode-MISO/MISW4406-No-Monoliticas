import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import json

from seguridad.modulos.hippa.infraestructura.schema.v1.eventos import EventoValidacionHippaCreada
from seguridad.modulos.hippa.infraestructura.schema.v1.comandos import ComandoCrearValidacionHippa
from seguridad.seedwork.infraestructura import utils

from seguridad.modulos.anonimizacion.aplicacion.mapeadores import MapeadorAnonimizacionDTOJson
from seguridad.modulos.anonimizacion.aplicacion.servicios import ServicioAnonimizacion

def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-hippa', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='seguridad-sub-eventos', schema=AvroSchema(EventoValidacionHippaCreada))

        print("oo-------> hippa_suscribirse_a_eventos()")
        while True:
            mensaje = consumidor.receive()
#########################################
            print(f'Evento recibido: {mensaje.value().data}')
#########################################
            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_comandos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comandos-hippa', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='seguridad-sub-comandos', schema=AvroSchema(ComandoCrearValidacionHippa))
#########################################        
        print("oo-------> hippa_suscribirse_a_comandos()")
#########################################

        while True:
            mensaje = consumidor.receive()
            print(f'oo-------> hippa:  Comando recibido: {mensaje.value().data}')
            consumidor.acknowledge(mensaje)
            
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()