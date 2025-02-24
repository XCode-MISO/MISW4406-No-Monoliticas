import pulsar
from pulsar.schema import *

from seguridad.modulos.anonimizacion.infraestructura.schema.v1.eventos import EventoAnonimizacionCreada, AnonimizacionCreadaPayload
from seguridad.modulos.anonimizacion.infraestructura.schema.v1.comandos import ComandoCrearAnonimizacion, ComandoCrearAnonimizacionPayload
from seguridad.seedwork.infraestructura import utils

import datetime

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(EventoAnonimizacionCreada))
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del evento
        payload = AnonimizacionCreadaPayload(
            id_reserva=str(evento.id_reserva), 
            id_cliente=str(evento.id_cliente), 
            estado=str(evento.estado), 
            fecha_creacion=int(unix_time_millis(evento.fecha_creacion))
        )
        evento_integracion = EventoAnonimizacionCreada(data=payload)
        self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoAnonimizacionCreada))

    def publicar_comando(self, comando, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del comando
        payload = ComandoCrearAnonimizacionPayload(
            id=str(comando.id)
        )
        comando_integracion = ComandoCrearAnonimizacion(data=payload)
        self._publicar_mensaje(comando_integracion, topico, AvroSchema(ComandoCrearAnonimizacion))
