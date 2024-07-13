from flask import Blueprint, jsonify, request

from controllers.usuarioController import UsuarioController
from flask_login import current_user, login_user, login_required, logout_user

from models.usuarioModel import Usuarios


usuario_bp = Blueprint("usuario", __name__)


@usuario_bp.route("/registrar-usuario", methods=["GET", "POST"])
def registrar_usuario():
    data = request.get_json()
    if request.method == "POST":
        return UsuarioController.registrar_usuario(data)
    else:
        return jsonify({'mensaje:': 'no es método POST'})
    

@usuario_bp.route("/iniciar-sesion-usuario", methods=["GET", "POST"])
def iniciar_sesion_usuario():
    data = request.get_json()
    if request.method == "POST":
        return UsuarioController.iniciar_sesion_usuario(data)
    else:
        return jsonify({'mensaje:': 'no es método POST'})

@usuario_bp.route("/usuario-actual", methods=["GET"])
def usuario_actual():
    return UsuarioController.usuario_actual()
        
#en cada una verificar por current user
@usuario_bp.route("/editar-cuenta-usuario", methods=["GET", "PATCH"])
@login_required
def editar_cuenta_usuario():
    data = request.get_json()
    return UsuarioController.editar_usuario(data)

@usuario_bp.route("/cerrar-sesion-usuario", methods=["GET"])
@login_required
def cerrar_sesion_usuario():
    return UsuarioController.cerrar_sesion_usuario()



