import pulsar
from pulsar.schema import *

from seguridad.modulos.anonimizacion.infraestructura.schema.v1.eventos import AnonimizacionAgregada, AnonimizacionAgregadaPayload
from seguridad.modulos.anonimizacion.infraestructura.schema.v1.comandos import ComandoCrearAnonimizacion, ComandoCrearAnonimizacionPayload
from seguridad.seedwork.infraestructura import utils

import datetime

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(AnonimizacionAgregada))
        publicador.send(mensaje)
        cliente.close()
    
    def _publicar_mensaje_comando(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(ComandoCrearAnonimizacion))
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento, topico):
        payload = AnonimizacionAgregadaPayload(
            id_anonimizacion=str(evento.id_reserva), 
            estado=str(evento.estado), 
            fecha_creacion=int(unix_time_millis(evento.fecha_creacion))
        )
        evento_integracion = AnonimizacionAgregada(data=payload)
        self._publicar_mensaje(evento_integracion, topico, AvroSchema(AnonimizacionAgregada))

    def publicar_comando(self, comando, topico):
        payload = ComandoCrearAnonimizacionPayload(
            fecha_creacion  = comando.fecha_creacion,
            fecha_actualizacion = comando.fecha_actualizacion,
            id = comando.id,
            nombre = comando.nombre,
            imagen = comando.imagen,
            fecha_fin = comando.fecha_fin
        )
        comando_integracion = ComandoCrearAnonimizacion(data=payload)
        self._publicar_mensaje_comando(comando_integracion, topico, AvroSchema(ComandoCrearAnonimizacion))