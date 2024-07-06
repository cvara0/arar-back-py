from database.db import db
from flask_login import UserMixin, login_user
from werkzeug.security import chek_password_hash, generate_password_hash
from flask import jsonify

class Usuario(db.Model, UserMixin):
    id_usuario = db.Column(db.Integer, primary_key = True)
    id_tipo_usuario = db.Column(db.SmallInteger, nullable = False)
    nombre = db.Column(db.String(64), nullable = False)
    apellido = db.Column(db.String(64), nullable = False)
    email = db.Column(db.String(32), nullable = False, unique = True)
    clave = db.Column(db.String(128), nullable = False)
    foto = db.Column(db.Text, nullable = False, default='https://i.postimg.cc/s22QHwdL/image.png')
    
    def __init__(self, id_tipo_usuario, nombre, apellido, email, clave, foto):
        self.id_tipo_usuario = id_tipo_usuario
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.clave = generate_password_hash(clave)
        self.foto = foto
        
    def verificar_clave(self, clave):
        return chek_password_hash(self.clave, clave)
    
    def a_diccionario(self):
        return {
            'id_tipo_usuario' : self.id_tipo_usuario,
            'nombre' : self.nombre,
            'apellido' : self.apellido,
            'email' : self.email,
            'clave' : self.clave,
            'foto' : self.foto
        }
    
    def registrar(self):
        try:
            db.session.add(self)
            login_user(self)
            return jsonify({'mensaje:': 'Cuenta creada con exito', 'Usuario' : self.a_diccionario()}), 201
        except:
            db.session.rollback()
            return jsonify({'mensaje:': 'error al agregar usuario'}), 500
        finally:
            db.session.commit()
        
    @staticmethod
    def traer_por_email(email):
        return Usuario.query.filter_by(email = email).first() #metodo posible gracias a herencia bd.model
    
    @staticmethod
    def traer_por_id(id_usuario):
        return Usuario.query.get(id_usuario)
    
    def iniciar_sesion(self):
        login_user(self)
        
    def cerrar_sesion(self):
        pass
    
    def __repr__(self):
        return f'<Usuario {self.email}>'