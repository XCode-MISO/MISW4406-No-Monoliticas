import datetime
import traceback
from autorizacion.modulos.validacion_usuario.infraestructura.schema.v1.comandos import ComandoErrorValidacion_Usuario, ComandoErrorValidacion_UsuarioPayload, CrearValidacion_Usuario
from autorizacion.modulos.validacion_usuario.infraestructura.schema.v1.eventos import ErrorValidacion_Usuario, ErrorValidacion_UsuarioPayload, Validacion_UsuarioAgregada, Validacion_UsuarioAgregadaPayload
from autorizacion.seedwork.dominio.eventos import EventoDominio
from ingestion_datos import utils
from ingestion_datos.aplicacion.comandos import ComandoIngerirDatos, IngestionDatosPayload, ComandoRevertirIngestionDatos, RevertirIngestionDatosPayload
from ingestion_datos.dominio.eventos import EventoIngestion, IngestionFinalizada, IngestionCancelada
from seguridad.modulos.anonimizacion.infraestructura.schema.v1.eventos import AnonimizacionAgregada
from seguridad.seedwork.aplicacion.sagas import CoordinadorOrquestacion, Fin, Inicio, Transaccion, Paso
from seguridad.modulos.anonimizacion.infraestructura.schema.v1.comandos import CrearAnonimizacion
from orquestrador.config.db import get_db
from orquestrador.dto import OrquestracionLog
from seguridad.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion as EventoIntegracionSeg
from autorizacion.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion as EventoIntegracionAuth


class CoordinadorProcesamientoDatos(CoordinadorOrquestacion):

    def inicializar_pasos(self):
        self.pasos = [
            Inicio(index=0),
            Transaccion(index=1, comando=CrearValidacion_Usuario,
                        evento=Validacion_UsuarioAgregada, error=ErrorValidacion_Usuario, compensacion=ComandoErrorValidacion_Usuario),
            Transaccion(index=2, comando=ComandoIngerirDatos,
                        evento=IngestionFinalizada, error=IngestionCancelada, compensacion=ComandoRevertirIngestionDatos),
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
        print(f"Orquestracion loggeando: {mensaje}")
        db = next(get_db())
        db.add(
            OrquestracionLog(
                fecha=datetime.datetime.now(),
                nombre=type(mensaje),
                id_evento=mensaje.id
            )
        )
        db.commit()

    async def publicar_comando(self, evento: EventoDominio, tipo_comando: type):
        comando = self.construir_comando(evento, tipo_comando)
        print(f"Comando construido: {comando}")
        if isinstance(comando, CrearValidacion_Usuario):
            from autorizacion.modulos.validacion_usuario.infraestructura.despachadores import Despachador
            despachador = Despachador()
            topic = "public/default/comandos-validacion_usuario"
            print(f'Publicando comando: {comando} en topic: {topic}')
            despachador.publicar_comando(comando, topic)
            self.persistir_en_saga_log(comando)
        elif isinstance(comando, ComandoErrorValidacion_Usuario):
            from autorizacion.modulos.validacion_usuario.infraestructura.despachadores import Despachador
            despachador = Despachador()
            topic = "public/default/comandos-error_usuario"
            print(f'Publicando comando: {comando} en topic: {topic}')
            despachador.publicar_comando_error(comando, topic)
            self.persistir_en_saga_log(comando)
        elif isinstance(comando, ComandoIngerirDatos):
            from ingestion_datos.infraestructura.despachadores import Despachador
            despachador = Despachador()
            topic = "public/default/comando-ingestion-datos"
            print(f'Publicando comando: {comando} en topic: {topic}')
            despachador.publicar_mensaje(comando, topic)
            self.persistir_en_saga_log(comando)
        elif isinstance(comando, ComandoRevertirIngestionDatos):
            from ingestion_datos.infraestructura.despachadores import Despachador
            despachador = Despachador()
            topic = "public/default/comando-revetir-ingestion-datos"
            print(f'Publicando comando: {comando} en topic: {topic}')
            despachador.publicar_mensaje(comando, topic)
            self.persistir_en_saga_log(comando)
        elif isinstance(comando, CrearAnonimizacion):
            from seguridad.modulos.anonimizacion.infraestructura.despachadores import Despachador
            despachador = Despachador()
            topic = "public/default/comandos-anonimizacion"
            print(f'Publicando comando: {comando} en topic: {topic}')
            despachador.publicar_comando(comando, topic)
            self.persistir_en_saga_log(comando)
        else:
            raise NotImplementedError(
                f"Comando no ha sido implementado {comando}")
        print("Finalizo publicar comando!")

    def construir_comando(self, evento: EventoDominio, tipo_comando: type):
        # TODO Transforma un evento en la entrada de un comando
        # Por ejemplo si el evento que llega es ReservaCreada y el tipo_comando es PagarReserva
        # Debemos usar los atributos de ReservaCreada para crear el comando PagarReserva
        print(f"Comando: {tipo_comando} y evento: {evento}")
        if isinstance(evento, Validacion_UsuarioAgregada) and tipo_comando == CrearValidacion_Usuario:
            datos = evento.data
            return CrearValidacion_Usuario(
                id=datos.id_validacion_usuario,
                fecha_actualizacion=utils.datetime_a_str(
                    utils.millis_a_datetime(utils.time_millis())),
                fecha_fin=utils.datetime_a_str(
                    utils.millis_a_datetime(utils.time_millis())),
                fecha_validacion=utils.datetime_a_str(
                    utils.millis_a_datetime(datos.fecha_validacion)),
                imagen=datos.imagen,
                nombre=datos.nombre,
                usuario=datos.id_validacion_usuario
            )
        # compensacion
        elif isinstance(evento, ErrorValidacion_Usuario) and tipo_comando == ComandoErrorValidacion_Usuario:
            datos = evento.data
            print(f"evento: {datos}")
            payload = ComandoErrorValidacion_UsuarioPayload(
                nombre=datos.nombre,
            )
            print(f'payload === {payload}')
            return ComandoErrorValidacion_Usuario(
                time=utils.time_millis(),
                data=payload
            )
        elif isinstance(evento, IngestionFinalizada) and tipo_comando == ComandoIngerirDatos:
            print(f"evento: {evento}")
            payload = IngestionDatosPayload(
                id_correlacion=str(evento.ingestion_id),
                imagen=r'{}'.format(evento.imagen),
                nombre=evento.nombre,
                fecha_creacion=int(utils.str_date_time(
                    evento.fecha_creacion).timestamp() * 1000),
            )
            print(f'payload === {payload}')
            return ComandoIngerirDatos(
                time=utils.time_millis(),
                data=payload
            )
        elif isinstance(evento, IngestionCancelada) and tipo_comando == ComandoRevertirIngestionDatos:
            print(f"evento: {evento}")
            payload = RevertirIngestionDatosPayload(
                id_correlacion=str(evento.ingestion_id)
            )
            print(f'payload === {payload}')
            return ComandoRevertirIngestionDatos(
                time=utils.time_millis(),
                data=payload
            )
        elif isinstance(evento, AnonimizacionAgregada) and tipo_comando == CrearAnonimizacion:
            return CrearAnonimizacion(
                fecha_actualizacion=utils.datetime_a_str(
                    datetime.datetime.now()),
                fecha_creacion=utils.datetime_a_str(
                    utils.millis_a_datetime(evento.data.fecha_creacion)),
                fecha_fin=None,
                id=evento.data.id_anonimizacion,
                imagen=evento.data.imagen,
                nombre=evento.data.nombre,
            )
        # TODO: compensacion
        else:
            raise NotImplementedError("No tiene un comando")
        ...


# TODO Agregue un Listener/Handler para que se puedan redireccionar eventos de dominio

    async def oir_mensaje(self, mensaje):
        print(f"oirmensaje: {mensaje}")
        print(f"oirmensaje tipo: {type(mensaje)}")
        if isinstance(mensaje, EventoDominio):
            await self.procesar_evento(mensaje)
        elif isinstance(mensaje, EventoIngestion):
            print(f"Mensaje: ${mensaje}")
            evento = mensaje.ingestion_finalizada if mensaje.datacontenttype == "IngestionFinalizada" else mensaje.ingestion_cancelada
            print(f"Type: {type(evento)}")
            await self.procesar_evento(evento)
        elif isinstance(mensaje, EventoIntegracionSeg):
            print(f"Mensaje: ${mensaje}")
            evento = mensaje if isinstance(
                mensaje, AnonimizacionAgregada) else None
            print(f"Type: {type(evento)}")
            await self.procesar_evento(evento)
        elif isinstance(mensaje, Validacion_UsuarioAgregada):
            print(f"Mensaje: ${mensaje}")
            print(f"Type: {type(mensaje)}")
            await self.procesar_evento(mensaje)
        elif isinstance(mensaje, ErrorValidacion_Usuario):
            print(f"Mensaje: ${mensaje}")
            print(f"Type: {type(mensaje)}")
            await self.procesar_evento(mensaje)
        else:
            traceback.print_exc()
            raise NotImplementedError(
                f"El mensaje: {mensaje} no es evento de Dominio")
