from flask import Blueprint, jsonify, render_template, request
from sqlalchemy import desc
from models.obraModel import Obras
from database.db import db
from flask_login import current_user, login_user, login_required, logout_user
from controllers.obraController import ObraController

obra_bp = Blueprint("obra", __name__)


@login_required
@obra_bp.route("/mis-obras/registrar-obra", methods=["GET", "POST"])
def registrar_obra():
    if request.method == "POST":
        data = {
            "id_tipo_obra": request.form.get("id_tipo_obra"),
            "titulo": request.form.get("titulo"),
            "descripcion": request.form.get("descripcion"),
            "id_usuario": request.form.get("id_usuario"),
        }
        file = request.files["foto"]
        return ObraController.registrar_obra(data, file)
    else:
        return jsonify({"mensaje:": "no es método POST"})


@obra_bp.route("/obras/<int:id_tipo_obra>", methods=["GET"])
def obras_por_id_tipo_obra(id_tipo_obra):
    return ObraController.traer_por_id_tipo_obra(id_tipo_obra)


@login_required
@obra_bp.route("/mis-obras/<int:id_usuario_actual>", methods=["GET"])
def mis_obras(id_usuario_actual):
    return ObraController.traer_por_id_usuario_actual(id_usuario_actual)


@login_required
@obra_bp.route("/mis-obras/editar-obra", methods=["GET", "PATCH"])
def editar_obra():
    if request.method == "PATCH":
        data = {
            "id_obra": request.form.get("id_obra"),
            "id_tipo_obra": request.form.get("id_tipo_obra"),
            "titulo": request.form.get("titulo"),
            "descripcion": request.form.get("descripcion")
        }
        file = request.files["foto"]
        return ObraController.editar_obra(data,file)
    else:
        return jsonify({"mensaje:": "no es método PATCH"})


@login_required
@obra_bp.route("/mis-obras/eliminar-obra/<int:id_obra>", methods=["GET", "DELETE"])
def eliminar_obra(id_obra):
    if request.method == "DELETE":
        return ObraController.eliminar_obra(id_obra)
    else:
        return jsonify({"mensaje:": "no es método DELETE"})
