import os
from sqlalchemy import desc
import sqlalchemy
from models.obraModel import Obras
from database.db import db
from flask import g, jsonify, send_from_directory, session
from flask_login import current_user, login_user, login_required, logout_user
from auth.login import lm
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from models.usuarioModel import Usuarios


class ObraController:

    @staticmethod
    def registrar_obra(data, file):
        mensaje = ()
        try:
            if not ObraController.traer_foto_por_nombre(secure_filename(file.filename)):
                # ruta_base = os.path.dirname(__file__)
                nombre_seguro = secure_filename(file.filename)
                ruta_de_subida = os.path.join("./static/fotos", nombre_seguro)
                obra = Obras(
                    data.get("id_usuario"),
                    data.get("id_tipo_obra"),
                    nombre_seguro,
                    data.get("titulo"),
                    data.get("descripcion"),
                )
                try:
                    file.save(ruta_de_subida)
                    db.session.add(obra)
                    db.session.commit()
                    mensaje = jsonify(
                        {"mensaje": "Obra registrada con èxito", "cod": 0}
                    )
                except:
                    db.session.rollback()
                    mensaje = jsonify({"mensaje": "error al agregar obra", "cod": 1})
            else:
                mensaje = jsonify(
                    {"mensaje": "esta imagen ya existe o el campo esta vacío", "cod": 2}
                )
        except:
            mensaje = jsonify(
                {"mensaje": "error en el envio de datos, verifique formato", "cod": 3}
            )
        return mensaje

    @staticmethod
    def traer_foto_por_nombre(nombre):
        return (
            db.session.execute(db.select(Obras).filter(Obras.foto.like(f"%{nombre}%")))
            .scalars()
            .all()
        )

    @staticmethod
    def traer_por_id(obra_id):
        return Obras.query.get(obra_id)

    @staticmethod
    def traer_por_id_usuario_actual(id_usuario):
        obras = (
            db.session.query(Obras)
            .filter(Obras.id_usuario == id_usuario)
            .order_by(desc(Obras.id_obra))
        )
        obras_de_usuario_actual = [
            {
                "id_obra": obra.id_obra,
                "id_tipo_obra": obra.id_tipo_obra,
                "foto": obra.foto,
                "titulo": obra.titulo,
                "descripcion": obra.descripcion,
                "id_usuario": obra.id_usuario,
            }
            for obra in obras
        ]
        return jsonify(obras_de_usuario_actual)

    @staticmethod
    def traer_por_id_tipo_obra(id_tipo_obra):
        obras = (
            db.session.query(
                Obras,
                Usuarios.nombre,
                Usuarios.apellido,
                Usuarios.telefono,
                Usuarios.id_tipo_usuario,
                Usuarios.id_usuario,
            )
            .join(Usuarios)
            .filter(Obras.id_tipo_obra == id_tipo_obra)
            .order_by(desc(Obras.id_obra))
        )
        obras_con_usuario = [
            {
                "id_obra": obra.id_obra,
                "id_tipo_obra": obra.id_tipo_obra,
                "foto": obra.foto,
                "titulo": obra.titulo,
                "descripcion": obra.descripcion,
                "nombre": nombre,
                "apellido": apellido,
                "telefono": telefono,
                "id_tipo_usuario": id_tipo_usuario,
                "id_usuario": id_usuario,
            }
            for obra, nombre, apellido, telefono, id_tipo_usuario, id_usuario in obras
        ]
        return jsonify(obras_con_usuario)

    @staticmethod
    def editar_obra(data):
        mensaje = None
        try:
            obra = Obras.query.get(data.get("id_obra"))
            print(obra)
            if data.get("id_tipo_obra"):
                obra.id_tipo_obra = data.get("id_tipo_obra")
            """ if file.filename is not None:
                if not ObraController.traer_foto_por_nombre(secure_filename(file.filename)):
                    ruta_de_subida = os.path.join("./static/fotos", obra.foto)
                    if os.path.exists(ruta_de_subida):
                        os.remove(ruta_de_subida)
                    nombre_seguro = secure_filename(file.filename)
                    ruta_de_subida = os.path.join("./static/fotos", nombre_seguro)
                    file.save(ruta_de_subida)
                    obra.foto = nombre_seguro """
         
        
            if data.get("titulo"):
                obra.titulo = data.get("titulo")
            if data.get("descripcion"):
                obra.descripcion = data.get("descripcion")
            db.session.commit()
            mensaje = jsonify({"mensaje": "Obra actualizada con éxito", "cod": 0})
        except:
            db.session.rollback()
            mensaje = jsonify({"mensaje:": "error al actualizar obra", "cod": 1})
        return mensaje

    @staticmethod
    def eliminar_obra(id_obra):
        mensaje = ()
        try:
            obra = Obras.query.get(id_obra)
            ruta_de_subida = os.path.join("./static/fotos", obra.foto)
            if os.path.exists(ruta_de_subida):
                os.remove(ruta_de_subida)
            db.session.delete(obra)
            db.session.commit()
            mensaje = jsonify({"mensaje": "Obra eliminada", "cod": 0})
        except:
            db.session.rollback()
            mensaje = jsonify(
                {"mensaje:": "error al eliminar obra desde flask", "cod": 1}
            )
        return mensaje
