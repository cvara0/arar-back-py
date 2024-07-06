from flask import Blueprint, jsonify, render_template, request
from models.obraModel import Obras
from database.db import db
from auth.login import login_required

obra_bp = Blueprint('obra',__name__)

@login_required
@obra_bp.route('/agregar-obra', methods=["GET", "POST"])
def agregar_obra():
    data = request.get_json()
    #if request.method == "POST":
    obra = Obras(
        id_tipo_obra = data['id_tipo_obra'],
        descripcion = data['descripcion'],
    )
    try:
        db.session.add(obra)
        return jsonify({'mensaje:': 'obra agregada con exito', 'obra' : obra.a_diccionario()}), 201
    except:
        db.session.rollback()
        return jsonify({'mensaje:': 'error al agregar'})
    finally:
        db.session.commit()

@obra_bp.route('/obras-de-arte', methods=["GET"])
def arte_traer_todo(): 
    obras = db.session.execute(db.select(Obras).order_by(Obras.id_obra)).scalars()
    return jsonify({'obras:': [obra.serialize() for obra in obras]})

@obra_bp.route('/obra-de-arte/<id_obra>', methods=["GET"])
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
    return 'editar obra'