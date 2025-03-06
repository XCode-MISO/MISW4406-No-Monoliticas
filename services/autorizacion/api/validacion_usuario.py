import autorizacion.seedwork.presentacion.api as api
import json
from flask import redirect, render_template, request, session, url_for
from flask import Response

from autorizacion.seedwork.dominio.excepciones import ExcepcionDominio
from autorizacion.modulos.validacion_usuario.aplicacion.mapeadores import MapeadorValidacion_UsuarioDTOJson
from autorizacion.modulos.validacion_usuario.aplicacion.servicios import ServicioValidacion_Usuario
from autorizacion.modulos.validacion_usuario.aplicacion.queries.obtener_validacion_usuario import ObtenerValidacion_Usuario
from autorizacion.modulos.validacion_usuario.aplicacion.comandos.crear_validacion_usuario import CrearValidacion_Usuario
from autorizacion.seedwork.aplicacion.queries import ejecutar_query
from autorizacion.modulos.validacion_usuario.infraestructura.despachadores import Despachador

bp = api.crear_blueprint('validacion_usuario', '/validacion_usuario')

@bp.route('/validacion_usuario', methods=['POST'])
def agregar_validacion_usuario():
    '''
    try:
        validacion_usuario_dict = request.json
        map_validacion_usuario = MapeadorValidacion_UsuarioDTOJson()
        validacion_usuario_dto = map_validacion_usuario.externo_a_dto(validacion_usuario_dict)
        sr = ServicioValidacion_Usuario()
        dto_final = sr.crear_validacion_usuario(validacion_usuario_dto)
        return map_validacion_usuario.dto_a_externo(dto_final)
    
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
    '''
    try:
        validacion_usuario_dict = request.json
        map_validacion_usuario = MapeadorValidacion_UsuarioDTOJson()
        validacion_usuario_dto = map_validacion_usuario.externo_a_dto(validacion_usuario_dict)
        #comando_usuario = Obtener_Usuario(validacion_usuario_dto.usuario)
        '''
        
        Instar proyecion de validacion de usuario
        
        if comando:
            return Response('{Usuario Valido}', status=202, mimetype='application/json')
        else:
            return Response('{Usuario Invalido}', status=400, mimetype='application/json')
        
        '''
        
        comando = CrearValidacion_Usuario(
            validacion_usuario_dto.fecha_validacion, 
            validacion_usuario_dto.fecha_actualizacion, 
            validacion_usuario_dto.id, 
            validacion_usuario_dto.usuario, 
            validacion_usuario_dto.nombre, 
            validacion_usuario_dto.imagen, 
            validacion_usuario_dto.fecha_fin
            )
        despachador = Despachador()
        despachador.publicar_comando(comando, 'public/default/comandos-validacion_usuario')
        return Response('{Usuario Valido}', status=202, mimetype='application/json')
    
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
    