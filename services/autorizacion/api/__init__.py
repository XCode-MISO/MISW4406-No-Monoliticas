import os
import threading
from flask import Flask, app, render_template, request, url_for, redirect, jsonify, session
from flask_swagger import swagger
import logging

basedir = os.path.abspath(os.path.dirname(__file__))

def registrar_handlers():
    import autorizacion.modulos.validacion_usuario.aplicacion
    import autorizacion.modulos.envio_imagen.aplicacion

def importar_modelos_alchemy():
    import autorizacion.modulos.validacion_usuario.infraestructura.dto
    import autorizacion.modulos.envio_imagen.infraestructura.dto

def comenzar_consumidor(app):
    import autorizacion.modulos.validacion_usuario.infraestructura.consumidores as validacion_usuario
    import autorizacion.modulos.envio_imagen.infraestructura.consumidores as envio_imagen

    # Suscripción a eventos
    threading.Thread(target=validacion_usuario.suscribirse_a_eventos).start()
    threading.Thread(target=envio_imagen.suscribirse_a_eventos).start()

    # Suscripción a comandos dentro del contexto de la app
    def suscribir_comandos():
        with app.app_context():  # Asegurar contexto de Flask
            validacion_usuario.suscribirse_a_comandos()
    def suscribir_comandos_envio_imagen():
        with app.app_context():  # Asegurar contexto de Flask
            envio_imagen.suscribirse_a_comandos()
    
    threading.Thread(target=suscribir_comandos).start()
    threading.Thread(target=suscribir_comandos_envio_imagen).start()

def create_app(configuracion={}):
    # Init la aplicación de Flask
    app = Flask(__name__, instance_relative_config=True)

    # Configuración de BD
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:adminadmin@localhost:3307/usuariosaludtech'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.secret_key = '9d58f98f-3ae8-4149-a09f-3a8c2012e32c'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['TESTING'] = configuracion.get('TESTING')

    # Inicializa la DB
    from autorizacion.config.db import init_db
    init_db(app)

    from autorizacion.config.db import db

    importar_modelos_alchemy()
    registrar_handlers()

    with app.app_context():
        db.create_all()

        if not app.config.get('TESTING'):
            print('comenzar_consumidor()')
            comenzar_consumidor(app)  # Pasamos la app para el contexto
        
        from autorizacion.modulos.validacion_usuario.infraestructura.dto import Usuario as UsuarioDTO
        try:
            db.session.add(UsuarioDTO(usuario='admin'))
            db.session.add(UsuarioDTO(usuario='admin1'))
            db.session.add(UsuarioDTO(usuario='admin2'))
            db.session.add(UsuarioDTO(usuario='admin3'))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print('Error al agregar la validacion_usuario:', e)

    # Importa Blueprints
    from . import validacion_usuario, envio_imagen

    # Registro de Blueprints
    app.register_blueprint(validacion_usuario.bp)
    app.register_blueprint(envio_imagen.bp)

    @app.route("/spec", methods=["GET"])
    def spec():
        swag = swagger(app)
        swag['info']['version'] = "1.0"
        swag['info']['title'] = "validacion_usuario de los Andes"
        return jsonify(swag)

    @app.route("/health", methods=["GET"])
    def health():
        return {"status": "up"}

    app.logger.setLevel(logging.DEBUG)
    return app
7