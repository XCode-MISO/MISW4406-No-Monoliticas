
import datetime
import inspect
from autorizacion.modulos.validacion_usuario.infraestructura.schema.v1.comandos import CrearValidacion_Usuario
from autorizacion.modulos.validacion_usuario.dominio.eventos import Validacion_UsuarioAgregada
from autorizacion.seedwork.dominio.eventos import EventoDominio
from ingestion_datos import utils
from ingestion_datos.aplicacion.comandos import ComandoIngerirDatos, IngestionDatosPayload
from ingestion_datos.dominio.eventos import EventoIngestion, IngestionFinalizada
from seguridad.modulos.anonimizacion.dominio.eventos import AnonimizacionAgregada
from seguridad.seedwork.aplicacion.sagas import CoordinadorOrquestacion, Fin, Inicio, Transaccion, Paso
from seguridad.modulos.anonimizacion.infraestructura.schema.v1.comandos import CrearAnonimizacion
from orquestrador.config import db
from orquestrador.dto import OrquestracionLog


class CoordinadorProcesamientoDatos(CoordinadorOrquestacion):

    def inicializar_pasos(self):
        self.pasos = [
            Inicio(index=0),
            Transaccion(index=1, comando=CrearValidacion_Usuario,
                        evento=Validacion_UsuarioAgregada, error=type(None), compensacion=type(None)),
            Transaccion(index=2, comando=ComandoIngerirDatos,
                        evento=IngestionFinalizada, error=type(None), compensacion=type(None)),
            Transaccion(index=3, comando=CrearAnonimizacion,
                        evento=AnonimizacionAgregada, error=type(None), compensacion=type(None)),
            Fin(index=5)
        ]

    def iniciar(self):
        self.persistir_en_saga_log(self.pasos[0])

    def terminar(self):
        self.persistir_en_saga_log(self.pasos[-1])

    def persistir_en_saga_log(self, mensaje):
        # TODO Persistir estado en DB
        # Probablemente usted podría usar un repositorio para ello
        db.add(
            OrquestracionLog(
                fecha=datetime.datetime.now(),
                nombre=mensaje.__class__,
                id_evento=mensaje.id
            )
        )
        db.commit()

    def publicar_comando(self,evento: EventoDominio, tipo_comando: type):
        comando = self.construir_comando(evento, tipo_comando)
        if isinstance(comando, CrearValidacion_Usuario):
            from autorizacion.modulos.validacion_usuario.infraestructura.despachadores import Despachador
            despachador = Despachador()
            topic = "public/default/comandos-validacion_usuario"
            print(f'Publicando comando: {comando} en topic: {topic}')
            despachador.publicar_comando(comando, topic)
        elif isinstance(comando, ComandoIngerirDatos):
            from ingestion_datos.infraestructura.despachadores import Despachador
            despachador = Despachador()
            topic = "public/default/comando-ingestion-datos"
            print(f'Publicando comando: {comando} en topic: {topic}')
            despachador.publicar_mensaje(comando, topic)
        elif isinstance(comando, CrearAnonimizacion):
            from seguridad.modulos.anonimizacion.infraestructura.despachadores import Despachador
            despachador = Despachador()
            topic = "public/default/comandos-anonimizacion"
            print(f'Publicando comando: {comando} en topic: {topic}')
            despachador.publicar_comando(comando, topic)
        else:
            raise NotImplementedError(f"Comando no ha sido implementado {comando}")

    def construir_comando(self, evento: EventoDominio, tipo_comando: type):
        # TODO Transforma un evento en la entrada de un comando
        # Por ejemplo si el evento que llega es ReservaCreada y el tipo_comando es PagarReserva
        # Debemos usar los atributos de ReservaCreada para crear el comando PagarReserva
        print(f"Comando: {tipo_comando} y evento: {evento}")
        if isinstance(evento, Validacion_UsuarioAgregada) and tipo_comando == CrearValidacion_Usuario:
            return CrearValidacion_Usuario(
                fecha_actualizacion=evento.fecha_evento,
                fecha_fin=utils.time_millis(),
                fecha_validacion=evento.fecha_evento,
                id=evento.id,
                imagen=evento.imagen,
                nombre=evento.nombre,
                usuario=evento.usuario
            )
        # TODO: compensacion
        elif isinstance(evento, IngestionFinalizada) and tipo_comando == ComandoIngerirDatos:
            print(f"evento: {evento}")
            return ComandoIngerirDatos(
                payload=IngestionDatosPayload(
                    id=evento.id,
                    fecha_creacion=utils.time_millis(),
                    imagen=evento.imagen,
                    nombre=evento.nombre,
                )
            )
        # TODO: compensacion
        elif isinstance(evento, AnonimizacionAgregada) and tipo_comando == CrearAnonimizacion:
            return CrearAnonimizacion(
                fecha_actualizacion=evento.fecha_evento,
                fecha_creacion=evento.fecha_creacion,
                fecha_fin=None,
                id=evento.id,
                imagen=evento.imagen,
                nombre=evento.nombre,
            )
        # TODO: compensacion
        else:
            raise NotImplementedError("No tiene un comando")
        ...


# TODO Agregue un Listener/Handler para que se puedan redireccionar eventos de dominio

    def oir_mensaje(self, mensaje):
        if isinstance(mensaje, EventoDominio):
            self.procesar_evento(mensaje)
        if isinstance(mensaje, EventoIngestion):
            print(f"Mensaje: ${mensaje}")
            evento = mensaje.ingestion_finalizada if mensaje.datacontenttype == "IngestionFinalizada" else mensaje.ingestion_cancelada
            print(f"Type: {type(evento)}")
            self.procesar_evento(evento)
        else:
            raise NotImplementedError("El mensaje no es evento de Dominio")
