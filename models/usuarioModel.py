from database.db import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

class Usuarios(db.Model, UserMixin):
    id_usuario = db.Column(db.Integer, primary_key=True)
    id_tipo_usuario = db.Column(db.SmallInteger, nullable=False)
    nombre = db.Column(db.String(64), nullable=False)
    apellido = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(32), nullable=False, unique=True)
    clave = db.Column(db.Text, nullable=False)
    telefono =  db.Column(db.String(16), nullable=False)
    foto = db.Column(db.Text, nullable=False)
    bio = db.Column(db.String(512), nullable=False)

    def __init__(
        self,
        id_tipo_usuario,
        nombre,
        apellido,
        email,
        clave,
        telefono,
        foto="https://i.postimg.cc/s22QHwdL/image.png",
        bio="Sin datos"
    ):
        self.id_tipo_usuario = id_tipo_usuario
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.clave = generate_password_hash(clave)
        self.telefono = telefono
        self.foto = foto
        self.bio = bio
        

    def a_diccionario(self):
        return {
            "id_tipo_usuario": self.id_tipo_usuario,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "telefono": self.telefono,
            "foto": self.foto,
            "bio": self.bio
        }
    
    #tiene que ir aca por la documentacion de alchemy
    def get_id(self):
        return self.id_usuario
            
    def __repr__(self):
        return f"<Usuario {self.email}>"
