from fastapi import FastAPI
import asyncio

from uvicorn.config import LOGGING_CONFIG

from pydantic import BaseSettings
from typing import Any

from orquestrador.config.db import Base, engine
from orquestrador.orquestrador import CoordinadorProcesamientoDatos
from orquestrador.consumidores import suscribirse_a_topico
from autorizacion.modulos.validacion_usuario.infraestructura.schema.v1.eventos import Validacion_UsuarioAgregada
from ingestion_datos.dominio.eventos import EventoIngestion
from seguridad.modulos.anonimizacion.infraestructura.schema.v1.eventos import AnonimizacionAgregada

class Config(BaseSettings):
    APP_VERSION: str = "1"

settings = Config()
app_configs: dict[str, Any] = {"title": "orquestrador "}

app = FastAPI(**app_configs)
tasks = list()

@app.on_event("startup")
async def app_startup():
    global tasks

    
    orquestrador = CoordinadorProcesamientoDatos()
    orquestrador.inicializar_pasos()
    
    task1 = asyncio.ensure_future(suscribirse_a_topico("public/default/evento-validacion_usuario", "sub-orquestrador-validacion", Validacion_UsuarioAgregada, orquestrador=orquestrador))
    #task1_f = asyncio.ensure_future(suscribirse_a_topico("public/default/evento-validacion_usuario", "sub-orquestrador", Validacion_UsuarioAgregada, orquestrador))
    task2 = asyncio.ensure_future(suscribirse_a_topico("public/default/evento-ingestion-datos", "sub-orquestrador-ingestion", EventoIngestion, orquestrador=orquestrador))
    task3 = asyncio.ensure_future(suscribirse_a_topico("public/default/eventos-anonimizacion", "sub-orquestrador-anonimizacion", AnonimizacionAgregada, orquestrador=orquestrador))
    #task3_F = asyncio.ensure_future(suscribirse_a_topico("public/default/comando-revetir-orquestrador", "sub-orquestrador", AnonimizacionAgregada, orquestrador))
    tasks.append(task1)
    tasks.append(task2)
    tasks.append(task3)
    Base.metadata.create_all(engine)

    
@app.on_event("shutdown")
def shutdown_event():
    global tasks
    for task in tasks:
        task.cancel()