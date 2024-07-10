from sqlalchemy import desc
import sqlalchemy
from models.obraModel import Obras
from database.db import db
from flask import jsonify
from flask_login import current_user, login_user, login_required, logout_user
from auth.login import lm
from werkzeug.security import check_password_hash, generate_password_hash

from models.usuarioModel import Usuarios


class ObraController():
    
    @staticmethod
    def registrar_obra(data):
        mensaje = ()
        try:
            if ObraController.traer_por_foto(data["foto"]) == []:
                obra = Obras(
                            current_user.id_usuario,
                            data["id_tipo_obra"],
                            data["foto"],
                            data["titulo"],
                            data["descripcion"]
                            )
                try:
                    db.session.add(obra)
                    db.session.commit()
                    mensaje = jsonify({"Obra registrada": obra.a_diccionario()}),201
                except:
                    db.session.rollback()
                    mensaje = jsonify({"mensaje:": "error al agregar obra"}), 500
            else:
                mensaje = jsonify({"mensaje:": "esta imagen ya existe o el campo esta vacío"})
        except:
            mensaje = jsonify({'mensaje:': 'error en el envio de datos, verifique formato'})
        return mensaje
    
    @staticmethod
    def traer_por_foto(foto):
        return db.session.execute(db.select(Obras).filter(Obras.foto.like(f"%{foto}%"))).scalars().all()

    @staticmethod
    def traer_por_id_tipo_obra(id_tipo_obra):
        obras = db.session.query(Obras, Usuarios.nombre, Usuarios.apellido) \
                      .join(Usuarios) \
                      .filter(Obras.id_tipo_obra == id_tipo_obra) \
                      .order_by(desc(Obras.id_obra))
        obras_con_usuario = [
                {
                    "id_obra" : obra.id_obra,
                    "id_tipo_obra" : obra.id_tipo_obra,
                    "foto" : obra.foto,
                    "titulo" : obra.titulo,
                    "descripcion" : obra.descripcion,
                    "nombre" : nombre,
                    "apellido" : apellido
                }
                for obra, nombre, apellido in obras
            ]
        return jsonify(obras_con_usuario)
    
"""@staticmethod
   def editar_obra(data): #seguir aca
        mensaje = ()
        try:
            usuario = current_user
            
            if data["id_tipo_usuario"]:
                usuario.id_tipo_usuario = data["id_tipo_usuario"]
                
            if data["nombre"]:
                usuario.nombre = data["nombre"]
                
            if data["apellido"]:
                usuario.apellido = data["apellido"]
                
            if data["clave"]:
                usuario.clave = generate_password_hash(data["clave"])
                
            if data["telefono"]:
                usuario.telefono = data["telefono"]

            db.session.commit()
            mensaje = jsonify({"Usuario actualizado": usuario.a_diccionario()}),201
        except:
            db.session.rollback()
            mensaje = jsonify({"mensaje:": "error al actualizar usuario"}), 500  
        
        return mensaje
 """
  