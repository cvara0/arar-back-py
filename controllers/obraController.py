from models.obraModel import Obras
from database.db import db
from flask import jsonify
from flask_login import current_user, login_user, login_required, logout_user
from auth.login import lm
from werkzeug.security import check_password_hash, generate_password_hash


class ObraController():
    
    @staticmethod
    def registrar_obra(data):
        mensaje = ()
        try:
            if ObraController.traer_por_foto(data["email"]) is None:
                obra = Obras(
                        data["id_usuario"],
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
                mensaje = jsonify({'mensaje:': 'ya existe una publicacion con esa imagen'})
        except:
            mensaje = jsonify({'mensaje:': 'error en el envio de datos, verifique formato'})
        return mensaje
    
    @staticmethod
    def traer_por_foto(foto):
        return Obras.query.filter_by(
            foto = foto
        ).first()  # metodo posible gracias a herencia bd.model

    @staticmethod
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
    
    def cerrar_sesion_usuario():
        mensaje = ()
        try:
            logout_user()
            mensaje = jsonify({'mensaje': 'Sesión finalizada'})
        except:
            mensaje = jsonify({'mensaje': 'Error al cerrar sesión'})
        return mensaje
  