from flask import Blueprint, jsonify, render_template, request
from sqlalchemy import desc
from models.obraModel import Obras
from database.db import db
from flask_login import current_user, login_user, login_required, logout_user
from controllers.obraController import ObraController

obra_bp = Blueprint('obra',__name__)

@login_required
@obra_bp.route('/registrar-obra', methods=["GET", "POST"])
def registrar_obra():
    data = request.get_json()
    if request.method == "POST":
        return ObraController.registrar_obra(data)
    else:
        return jsonify({'mensaje:': 'no es método POST'})

@obra_bp.route('/obras/<int:id_tipo_obra>', methods=["GET"])
def obras_por_id_tipo_obra(id_tipo_obra): 
    return ObraController.traer_por_id_tipo_obra(id_tipo_obra)
    

"""@obra_bp.route('/obra-de-arte/<id_obra>', methods=["GET"])
def arte_traer_por_id(): 
    obras = db.session.execute(db.select(Obras).order_by(Obras.id_obra)).scalars()
    return jsonify({'obras:': [obra.serialize() for obra in obras]})

@obra_bp.route('/artesanias')
def artesania_traer_todo():
    return 'traer todod artesania'

 @login_required
@obra_bp.route('/eliminar-obra/<id_obra>')
def eliminar(id_obra):
    return 'eliminar obra'

@login_required
@obra_bp.route('/editar-obra')
def editar():
    return 'editar obra' """