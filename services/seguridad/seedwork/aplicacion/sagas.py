from abc import ABC, abstractmethod
from seguridad.seedwork.aplicacion.comandos import Comando
from seguridad.seedwork.dominio.eventos import EventoDominio
from dataclasses import dataclass
from .comandos import ejecutar_commando
import uuid
import datetime

class CoordinadorSaga(ABC):
    id_correlacion: uuid.UUID

    @abstractmethod
    def persistir_en_saga_log(self, mensaje):
        ...

    @abstractmethod
    def construir_comando(self, evento: EventoDominio, tipo_comando: type) -> Comando:
        ...

    @abstractmethod
    def publicar_comando(self,evento: EventoDominio, tipo_comando: type):
        ...

    @abstractmethod
    def inicializar_pasos(self):
        ...
    
    @abstractmethod
    def procesar_evento(self, evento: EventoDominio):
        ...

    @abstractmethod
    def iniciar():
        ...
    
    @abstractmethod
    def terminar():
        ...

class Paso():
    id_correlacion: uuid.UUID
    fecha_evento: datetime.datetime
    index: int

@dataclass
class Inicio(Paso):
    index: int = 0

@dataclass
class Fin(Paso):
    index: int
    ...
@dataclass
class Transaccion(Paso):
    index: int
    comando: Comando
    evento: EventoDominio
    error: EventoDominio
    compensacion: Comando

class CoordinadorOrquestacion(CoordinadorSaga, ABC):
    pasos: list[Paso]
    index: int
    
    def obtener_paso_dado_un_evento(self, evento: EventoDominio):
        for i, paso in enumerate(self.pasos):
            if not isinstance(paso, Transaccion):
                continue
            if isinstance(evento, paso.evento) or isinstance(evento, paso.error):
                return paso, i
        raise Exception("Evento no hace parte de la transacción")
                
    def es_ultima_transaccion(self, index):
        return len(self.pasos) - index <= 1

    async def procesar_evento(self, evento: EventoDominio):
        paso, index = self.obtener_paso_dado_un_evento(evento)
        print(f"Paso: {paso} Indice: {index}")
        if self.es_ultima_transaccion(index) and not isinstance(evento, paso.error):
            print("Terminar procesar evento transaccion")
            self.terminar()
        elif isinstance(evento, paso.error):
            print("rollback")
            await self.publicar_comando(evento, self.pasos[index-1].compensacion)
        elif isinstance(evento, paso.evento):
            print("publicar siguiente")
            await self.publicar_comando(evento, self.pasos[index].comando)



