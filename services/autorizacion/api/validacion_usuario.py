import datetime
import uuid
import autorizacion.seedwork.presentacion.api as api
import json
from flask import redirect, render_template, request, session, url_for
from flask import Response

from autorizacion.seedwork.dominio.excepciones import ExcepcionDominio
from autorizacion.modulos.validacion_usuario.aplicacion.mapeadores import MapeadorValidacion_UsuarioDTOJson
from autorizacion.modulos.validacion_usuario.aplicacion.servicios import ServicioValidacion_Usuario
from autorizacion.modulos.validacion_usuario.aplicacion.queries.obtener_validacion_usuario import ObtenerValidacion_Usuario

from autorizacion.seedwork.aplicacion.queries import ejecutar_query
from autorizacion.modulos.validacion_usuario.infraestructura.despachadores import Despachador
from autorizacion.modulos.validacion_usuario.seedwork.infraestructura import utils

bp = api.crear_blueprint('validacion_usuario', '/validacion_usuario')

@bp.route('/validacion_usuario', methods=['POST'])
def agregar_validacion_usuario():    
    try:
        validacion_usuario_dict = request.json
        print(validacion_usuario_dict)
        despacharEventoUsuarioValido(validacion_usuario_dict)
        return Response('{Usuario Valido}', status=202, mimetype='application/json')        
        """ comando = CrearValidacion_Usuario(validacion_usuario_dto.fecha_validacion, validacion_usuario_dto.fecha_actualizacion, validacion_usuario_dto.id, validacion_usuario_dto.usuario, validacion_usuario_dto.nombre, validacion_usuario_dto.imagen, validacion_usuario_dto.fecha_fin)
        despachador = Despachador()
        despachador.publicar_comando(comando, 'public/default/comandos-validacion_usuario') """
        return Response('{Usuario Valido}', status=202, mimetype='application/json')
    
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/error_usuario', methods=['POST'])
def agregar_error_usuario():    
    from autorizacion.modulos.validacion_usuario.infraestructura.schema.v1.eventos import ErrorValidacion_UsuarioPayload

    try:
        data = request.json
        usuario = data["usuario"]
        despacharEventoErrorUsuario(usuario)  
        """ comando = ErrorValidacion_Usuario(usuario)
        despachador = Despachador()
        despachador.publicar_comando_error(comando, 'public/default/comandos-error_usuario') """     

        return Response('{Error Usuario}', status=202, mimetype='application/json')
    
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')


@bp.route('/usuario', methods=['GET'])
@bp.route('/usuario/<id>', methods=['GET'])
def dar_usuario(id=None):
    if id:
        query_resultado = ejecutar_query(ObtenerValidacion_Usuario(id))
        map_validacion_usuario = MapeadorValidacion_UsuarioDTOJson()
        return map_validacion_usuario.dto_a_externo(query_resultado.resultado)
    
    else:
        sr = ServicioValidacion_Usuario()
        return sr.obtener_todas_las_validacion_usuario()
    

from autorizacion.modulos.validacion_usuario.aplicacion.mapeadores import MapeadorValidacion_UsuarioDTOJson
from autorizacion.modulos.validacion_usuario.aplicacion.servicios import ServicioValidacion_Usuario
from autorizacion.modulos.validacion_usuario.infraestructura.schema.v1.eventos import ErrorValidacion_Usuario, Validacion_UsuarioAgregada, Validacion_UsuarioAgregadaPayload, ErrorValidacion_UsuarioPayload

def despacharEventoErrorUsuario(login_usuario):
    print(f"\n================> Usuario maligno detectado:", login_usuario)
    payload = ErrorValidacion_UsuarioPayload(
        nombre = login_usuario
    )
    evento = ErrorValidacion_Usuario(
        data=payload
    )
    print(f"\n================> evento: ", evento)
    despachador = Despachador()
    despachador.pub_mensaje_error(evento, 'public/default/evento-error-validacion-usuario')
    print("\n=================> Evento despachado!!!!!!!!!")    

def despacharEventoUsuarioValido(validacion_usuario_dict):
    print("\n=================> parametro dto: ", validacion_usuario_dict)
    evento = Validacion_UsuarioAgregada(
        data = Validacion_UsuarioAgregadaPayload(
            id_validacion_usuario = str(uuid.uuid4()),
            estado = "Inicio",
            fecha_validacion = utils.time_millis(),
            imagen = validacion_usuario_dict["imagen"],
            nombre = validacion_usuario_dict["usuario"]
        )
    )
    despachador = Despachador()
    despachador.pub_mensaje(evento, 'public/default/evento-validacion-usuario-finalizada')
    print("\n=================> Evento despachado!!!!!!!!!")    