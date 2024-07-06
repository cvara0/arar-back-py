from flask import Blueprint, jsonify, render_template, request
from models.usuarioModel import Usuarios
from database.db import db
from auth.login import login_manager, login_user, login_required, logout_user

usuario_bp = Blueprint('usuario',__name__)

@usuario_bp.route('/registrar-usuario', methods=["GET", "POST"])
def registrar_usuario():
    data = request.get_json()
    if request.method == "POST":
        usuario = Usuarios(
            data['id_tipo'],
            data['nombre'],
            data['apellido'],
            data['email'],
            data['clave'],
            data['foto']
        )
    respuesta = usuario.registrar()
    return respuesta
    #login_user(usuario)

@usuario_bp.route('/iniciar-sesion-usuario', methods=["GET", "POST"])
def iniciar_sesion_usuario():
    data = request.get_json()
    if request.method == "POST":
        usuario = Usuarios.traer_por_email(data['email'])
        if usuario is not None and usuario.verificar_clave(data['clave']):
                usuario.iniciar_sesion()

@login_required
@usuario_bp.route('/cuenta-usuario', methods=["GET", "POST"])
def cuenta_usuario():
    pass

@login_required
@usuario_bp.route('/cerrar-sesion-usuario')
def cerrar_sesion_usuario():
    logout_user()

@login_manager.user_loader
def cargar_usuario(id_usuario):
    return Usuarios.traer_por_id(id_usuario)