import pulsar
from pulsar.schema import *

from seguridad.modulos.hippa.infraestructura.schema.v1.eventos import EventoValidacionHippaCreada, ValidacionHippaPayload
from seguridad.modulos.hippa.infraestructura.schema.v1.comandos import ComandoCrearValidacionHippa, ComandoCrearValidacionHippaPayload
from seguridad.seedwork.infraestructura import utils

import datetime

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(EventoValidacionHippaCreada))
        publicador.send(mensaje)
        cliente.close()
    
    def _publicar_mensaje_comando(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=schema)
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del evento
        payload = ValidacionHippaPayload(
            id=str(evento.id), 
            estado=str(evento.estado), 
            image=str(evento.image)
        )
        evento_integracion = EventoValidacionHippaCreada(data=payload)
        self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoValidacionHippaCreada))

    def publicar_comando(self, comando, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del comando
        payload = ComandoCrearValidacionHippaPayload(
            id=str(comando.id)
            ,
        )
        comando_integracion = ComandoCrearValidacionHippa(data=payload)
        self._publicar_mensaje_comando(comando_integracion, topico, AvroSchema(ComandoCrearValidacionHippa))
