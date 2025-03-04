import pulsar
from pulsar.schema import *

from autorizacion.modulos.envio_imagen.infraestructura.schema.v1.eventos import EventoValidacionEnvio_ImagenCreada, ValidacionEnvio_ImagenPayload
from autorizacion.modulos.envio_imagen.infraestructura.schema.v1.comandos import ComandoCrearValidacionEnvio_Imagen, ComandoCrearValidacionEnvio_ImagenPayload
from autorizacion.seedwork.infraestructura import utils

import datetime

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(EventoValidacionEnvio_ImagenCreada))
        publicador.send(mensaje)
        cliente.close()
    
    def _publicar_mensaje_comando(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(ComandoCrearValidacionEnvio_Imagen))
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del evento
        payload = ValidacionEnvio_ImagenPayload(
            id=str(evento.id), 
            estado=str(evento.estado), 
            image=str(evento.image)
        )
        evento_integracion = EventoValidacionEnvio_ImagenCreada(data=payload)
        self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoValidacionEnvio_ImagenCreada))

    def publicar_comando(self, comando, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del comando
        payload = ComandoCrearValidacionEnvio_ImagenPayload(
            id=comando.id,
            image=comando.image,
            estado=comando.estado
        )
        comando_integracion = ComandoCrearValidacionEnvio_Imagen(data=payload)
        self._publicar_mensaje_comando(comando_integracion, topico, AvroSchema(ComandoCrearValidacionEnvio_Imagen))
