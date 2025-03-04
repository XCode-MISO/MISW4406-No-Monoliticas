from fastapi import FastAPI
import asyncio
import time
import traceback
import uvicorn

from pydantic import BaseSettings
from typing import Any

from ingestion_datos.dominio.eventos import EventoIngestion, IngestionCancelada, IngestionFinalizada
from ingestion_datos.aplicacion.comandos import ComandoIngerirDatos, ComandoRevertirIngestionDatos, RevertirIngestionDatosPayload, IngestionDatosPayload
from ingestion_datos.infraestructura.consumidores import suscribirse_a_topico
from ingestion_datos.infraestructura.despachadores import Despachador

from ingestion_datos.config.db import Base, engine

from . import utils

class Config(BaseSettings):
    APP_VERSION: str = "1"

settings = Config()
app_configs: dict[str, Any] = {"title": "ingestion-datos "}

app = FastAPI(**app_configs)
tasks = list()

@app.on_event("startup")
async def app_startup():
    global tasks
    task1 = asyncio.ensure_future(suscribirse_a_topico("evento-ingestion-datos", "sub-ingestion-datos", EventoIngestion))
    task2 = asyncio.ensure_future(suscribirse_a_topico("comando-ingestion-datos", "sub-com-ingestion-datos-crear", ComandoIngerirDatos))
    task3 = asyncio.ensure_future(suscribirse_a_topico("comando-revetir-ingestion-datos", "sub-com-ingestion-datos-revertir", ComandoRevertirIngestionDatos))
    tasks.append(task1)
    tasks.append(task2)
    tasks.append(task3)
    
    Base.metadata.create_all(engine)

@app.on_event("shutdown")
def shutdown_event():
    global tasks
    for task in tasks:
        task.cancel()

@app.get("/prueba-ingestion_datos_exitosa", include_in_schema=False)
async def prueba_ingestion_pagada() -> dict[str, str]:
    payload = IngestionFinalizada(
        id = "1232321321",
        id_correlacion = "389822434",
        ingestion_id = "6463454",
        imagen = 'https://upload.wikimedia.org/wikipedia/commons/3/32/Dark_Brandon.jpg',
        nombre = 'dark-brandon',
        fecha_creacion = utils.datetime_a_str(utils.millis_a_datetime(utils.time_millis())) 
    )

    evento = EventoIngestion(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=IngestionFinalizada.__name__,
        ingestion_finalizada = payload
    )
    print(f"PAYLOAD: {payload.__dict__}")
    despachador = Despachador()
    despachador.publicar_mensaje(evento, "evento-ingestion-datos")
    return {"status": "ok"}


@app.get("/health", include_in_schema=False)
async def health() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/", include_in_schema=False)
async def base() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/prueba-ingestion-datos-revertido", include_in_schema=False)
async def prueba_pago_revertido() -> dict[str, str]:
    payload = IngestionCancelada(
        id = "1232321321",
        id_correlacion = "389822434",
        ingestion_id = "6463454",
        fecha_actualizacion = utils.datetime_a_str(utils.millis_a_datetime(utils.time_millis()))
    )

    evento = EventoIngestion(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=IngestionCancelada.__name__,
        ingestion_cancelada = payload
    )
    despachador = Despachador()
    despachador.publicar_mensaje(evento, "evento-ingestion-datos")
    return {"status": "ok"}
    
@app.get("/prueba-ingestion-datos", include_in_schema=False)
async def prueba_pagar_ingestion() -> dict[str, str]:
    payload = IngestionDatosPayload(
        id_correlacion = "389822434",
        ingestion_id = "6463454",
        imagen = 'https://upload.wikimedia.org/wikipedia/commons/3/32/Dark_Brandon.jpg',
        nombre = 'dark-brandon'
    )

    comando = ComandoIngerirDatos(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=IngestionFinalizada.__name__,
        data = payload
    )
    despachador = Despachador()
    despachador.publicar_mensaje(comando, "comando-ingestion-datos")
    return {"status": "ok"}

@app.get("/prueba-revetir-ingestion-datos", include_in_schema=False)
async def prueba_revertir_pago() -> dict[str, str]:
    payload = RevertirIngestionDatosPayload(
        id = "1232321321",
        id_correlacion = "389822434",
        ingestion_id = "6463454",
    )

    comando = ComandoRevertirIngestionDatos(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=RevertirIngestionDatosPayload.__name__,
        data = payload
    )
    despachador = Despachador()
    despachador.publicar_mensaje(comando, "comando-revertir-ingestion-datos")
    return {"status": "ok"}