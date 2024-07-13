from sqlalchemy import desc
import sqlalchemy
from models.obraModel import Obras
from database.db import db
from flask import g, jsonify, session
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
    def traer_por_id(obra_id):
        return Obras.query.get(obra_id)
    
   
    @staticmethod
    def traer_por_id_usuario_actual(id_usuario):
        obras = db.session.query(Obras) \
                      .filter(Obras.id_usuario == id_usuario) \
                      .order_by(desc(Obras.id_obra))
        obras_de_usuario_actual = [
                        {
                            "id_obra" : obra.id_obra,
                            "id_tipo_obra" : obra.id_tipo_obra,
                            "foto" : obra.foto,
                            "titulo" : obra.titulo,
                            "descripcion" : obra.descripcion,
                            "id_usuario": obra.id_usuario
                        }
                        for obra in obras
                    ]
        return jsonify(obras_de_usuario_actual)

    @staticmethod
    def traer_por_id_tipo_obra(id_tipo_obra):
        obras = db.session.query(Obras, Usuarios.nombre, Usuarios.apellido, Usuarios.telefono, Usuarios.id_tipo_usuario, Usuarios.id_usuario) \
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
                    "apellido" : apellido,
                    "telefono" : telefono,
                    "id_tipo_usuario" : id_tipo_usuario,
                    "id_usuario" : id_usuario
                }
                for obra, nombre, apellido, telefono, id_tipo_usuario,id_usuario in obras
            ]
        return jsonify(obras_con_usuario)
    
    @staticmethod
    def editar_obra(data):
        mensaje = ()
        try:
            obra = Obras.query.get(data["id_obra"])
            if data["id_tipo_obra"]:
                        obra.id_tipo_obra = data["id_tipo_obra"] 
            if data["foto"]:
                        obra.foto = data["foto"] 
            if data["titulo"]:
                        obra.titulo = data["titulo"] 
            if data["descripcion"]:
                        obra.descripcion = data["descripcion"]
            db.session.commit()
            mensaje = jsonify({"mensaje": "Obra actualizada con éxito", "cod":0})
        except:
            db.session.rollback()
            mensaje = jsonify({"mensaje:": "error al actualizar obra", "cod":1})  
        return mensaje
    
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
  