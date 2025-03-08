import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import json
from datetime import datetime

from seguridad.modulos.anonimizacion.infraestructura.schema.v1.eventos import AnonimizacionAgregada, AnonimizacionAgregadaPayload, ErrorAnonimizacion
from seguridad.modulos.anonimizacion.infraestructura.schema.v1.comandos import ComandoCrearAnonimizacion, ComandoError_Anonimizacion
from seguridad.modulos.anonimizacion.aplicacion.mapeadores import MapeadorAnonimizacionDTOJson
from seguridad.modulos.anonimizacion.aplicacion.servicios import ServicioAnonimizacion
from seguridad.seedwork.infraestructura import utils
from seguridad.modulos.anonimizacion.infraestructura.despachadores import Despachador

#from seguridad.seedwork.aplicacion.comandos import ejecutar_commando
#from seguridad.modulos.anonimizacion.aplicacion.comandos.crear_anonimizacion import CrearAnonimizacion
#from seguridad.modulos.hippa.infraestructura.despachadores import Despachador
#from seguridad.modulos.hippa.aplicacion.comandos.crear_validacion_hippa import CrearValidacionHippa

def suscribirse_a_eventos():
    cliente = None
    topico = 'public/default/eventos-anonimizacion-finalizada'
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe(topico, consumer_type=_pulsar.ConsumerType.Shared,subscription_name='seguridad-sub-eventos', schema=AvroSchema(AnonimizacionAgregada))

        print("\n================> suscribirse_a_eventos()")
        while True:
            mensaje = consumidor.receive()
            print(f'\n================> Evento recibido: {mensaje.value().data}')
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
    topico = 'public/default/evento-error-anonimizacion'
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe(topico, consumer_type=_pulsar.ConsumerType.Shared,subscription_name='seguridad-sub-eventos', schema=AvroSchema(ErrorAnonimizacion))

        print("\n================> suscribirse_a_eventos_error()")
        while True:
            mensaje = consumidor.receive()
            print(f'\n========suscribirse_a_eventos_error()========> Evento recibido: {mensaje.value()}')
            try:
                comando = ErrorAnonimizacion("invalido")
                despachador = Despachador()
                despachador.publicar_comando_error(comando, 'public/default/comandos-error_anonimizacion')
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
        consumidor = cliente.subscribe('public/default/comandos-anonimizacion', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='seguridad-sub-comandos', schema=AvroSchema(ComandoCrearAnonimizacion))
        print("\n================> suscribirse_a_comandos()")
        while True:
            mensaje = consumidor.receive()
            print(f'\n================> Comando recibido: {mensaje.value().data}')
            anonimizacion_dict = mensaje.value().data.__dict__
            imagen = anonimizacion_dict['imagen']

            if (imagen == "invalida"):
                despacharEventoErrorValidacion(imagen)
            else:
                map_anonimizacion = MapeadorAnonimizacionDTOJson()
                anonimizacion_dto = map_anonimizacion.externo_a_dto(anonimizacion_dict)            
                sr = ServicioAnonimizacion()
                dto_final = sr.crear_anonimizacion(anonimizacion_dto)            
                despacharEventoAnonimizacionFinalizada(anonimizacion_dto)
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
        consumidor = cliente.subscribe('public/default/comandos-error_anonimizacion', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='seguridad-sub-comandos', schema=AvroSchema(ComandoError_Anonimizacion))
        print("\n================> suscribirse_a_comandos_error()")
        while True:
            mensaje = consumidor.receive()
            print(f'\n========suscribirse_a_comandos_error()========> Comando recibido: {mensaje.value().data}')
            consumidor.acknowledge(mensaje)
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos de error!')
        traceback.print_exc()
        if cliente:
            cliente.close()


def despacharEventoErrorValidacion(imagen):
    print(f"\n================> validacion defectuorsa:", imagen)
    evento = ErrorAnonimizacion(
        imagen = imagen
    )
    print(f"\n================> evento: ", evento)
    despachador = Despachador()
    despachador.pub_mensaje_error(evento, 'public/default/evento-error-anonimizacion')
    print("\n=================> Evento despachado!!!!!!!!!")    


def despacharEventoAnonimizacionFinalizada(dto_final):
    from datetime import datetime
    from seguridad.modulos.anonimizacion.infraestructura.despachadores import Despachador
    print("\n=================> parametro dto: ", dto_final)
    evento = AnonimizacionAgregadaPayload(
        id_anonimizacion="12345",
        estado="COMPLETADO",
        fecha_creacion=datetime.utcnow().isoformat()
    )
    print("\n=================> evento: ", evento)
    despachador = Despachador()
    despachador.publicar_evento(evento, 'public/default/eventos-anonimizacion-finalizada')
    print("\n=================> Evento despachado!!!!!!!!!")