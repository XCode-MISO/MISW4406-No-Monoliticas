"""Entidades del dominio de vuelos

En este archivo usted encontrará las entidades del dominio de vuelos

"""

from __future__ import annotations
from dataclasses import dataclass, field

import autorizacion.modulos.validacion_usuario.dominio.objetos_valor as ov
from autorizacion.modulos.validacion_usuario.dominio.eventos import Validacion_UsuarioAgregada, UsuarioAgregada
from autorizacion.seedwork.dominio.entidades import AgregacionRaiz, Entidad

@dataclass
class Validacion_Usuario(AgregacionRaiz):
    usuario: str = field(default_factory=str)
    nombre: str = field(default_factory=str)
    imagen: str = field(default_factory=str)
    fecha_fin: str = field(default_factory=str)

    def crear_validacion_usuario(self, validacion_usuario: Validacion_Usuario):
        self.usuario = validacion_usuario.usuario
        self.nombre = validacion_usuario.nombre
        self.imagen = validacion_usuario.imagen
        self.fecha_fin = validacion_usuario.fecha_fin
        self.agregar_evento(Validacion_UsuarioAgregada(id_reserva=self.id, usuario=self.usuario, fecha_validacion=self.fecha_validacion))

@dataclass
class Usuario(AgregacionRaiz):
    usuario: str = field(default_factory=str)

    def crear_usuario(self, usuario: Usuario):
        self.usuario = usuario.usuario
        self.agregar_evento(UsuarioAgregada(id_reserva=self.id,usuario=self.usuario,))