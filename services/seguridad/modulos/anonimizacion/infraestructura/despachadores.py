import pulsar
from pulsar.schema import *

from seguridad.modulos.anonimizacion.infraestructura.schema.v1.eventos import AnonimizacionAgregada, AnonimizacionAgregadaPayload, ErrorAnonimizacion
from seguridad.modulos.anonimizacion.infraestructura.schema.v1.comandos import ComandoCrearAnonimizacion, ComandoCrearAnonimizacionPayload
from seguridad.modulos.anonimizacion.infraestructura.schema.v1.comandos import ComandoError_Anonimizacion, ComandoError_AnonimizacionPayload
from seguridad.seedwork.infraestructura import utils

import datetime

epoch = datetime.datetime.utcfromtimestamp(0)

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
        print(f"Evento: {evento}")
        payload = AnonimizacionAgregadaPayload(
            id_anonimizacion=str(evento.id_anonimizacion), 
            estado=str(evento.estado), 
            fecha_creacion=evento.fecha_creacion,
            imagen=evento.imagen,
            nombre=evento.nombre
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

################################################################
    def _publicar_mensaje_comando_error(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(ComandoError_Anonimizacion))
        publicador.send(mensaje)
        cliente.close()

    def publicar_comando_error(self, comando, topico):
        payload = ComandoError_AnonimizacionPayload(
            imagen = comando.imagen
        )
        comando_integracion = ComandoError_Anonimizacion(data=payload)
        self._publicar_mensaje_comando_error(comando_integracion, topico, AvroSchema(ComandoError_Anonimizacion))
    
    def pub_mensaje_error(self, mensaje, topico):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(ErrorAnonimizacion))
        publicador.send(mensaje)
        cliente.close()
################################################################
