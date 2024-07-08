from models.usuarioModel import Usuarios
from database.db import db
from flask import jsonify
from flask_login import current_user, login_user, login_required, logout_user
from auth.login import lm
from werkzeug.security import check_password_hash, generate_password_hash


class UsuarioController():
    
    @staticmethod
    def registrar_usuario(data):
        mensaje = ()
        try:
            if UsuarioController.traer_por_email(data["email"]) is None:
                usuario = Usuarios(
                    data["id_tipo_usuario"],
                    data["nombre"],
                    data["apellido"],
                    data["email"],
                    data["clave"],
                    data["telefono"]
                )
                try:
                    db.session.add(usuario)
                    db.session.commit()
                    mensaje = jsonify({"Usuario registrado": usuario.a_diccionario()}),201
                except:
                    db.session.rollback()
                    mensaje = jsonify({"mensaje:": "error al agregar usuario"}), 500  
            else:
                mensaje = jsonify({'mensaje:': 'ya existe una cuenta con ese email'})
        except:
            mensaje = jsonify({'mensaje:': 'error en el envio de datos, verifique formato'})
        return mensaje
        
    @staticmethod
    def iniciar_sesion_usuario(data):
            mensaje = ()
            usuario = UsuarioController.traer_por_email(data["email"])
            if usuario is not None and UsuarioController.verificar_clave(usuario.clave, data["clave"]):
                try:
                    login_user(usuario)
                except:
                    mensaje = jsonify({'mensaje:': 'error inesperado al iniciar sesión'})
                mensaje = jsonify({'mensaje:': 'sesion iniciada', 'usuario': current_user.nombre})
            else:
                mensaje = jsonify({'mensaje:': 'email o contraseña incorrectos'})
            return mensaje

    @lm.user_loader
    def load_user(user_id):
        return UsuarioController.traer_por_id(int(user_id))

    @staticmethod
    def verificar_clave(clave_encontrada, clave_ingresada):
        return check_password_hash(clave_encontrada, clave_ingresada)

    @staticmethod
    def usuario_actual():
        mensaje = ()
        try:
           mensaje = jsonify({'usuario actual': Usuarios.a_diccionario(current_user)})
        except:
            mensaje = jsonify({'mensaje': 'Ningun usuario registrado'})
        return mensaje

    @staticmethod
    def traer_por_email(email):
        return Usuarios.query.filter_by(
            email=email
        ).first()  # metodo posible gracias a herencia bd.model

    @staticmethod
    def traer_por_id(user_id):
        return Usuarios.query.get(user_id)
    
    @staticmethod
    def editar_usuario(data):
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
  