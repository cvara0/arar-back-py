from database.db import db

class Obras(db.Model):
    id_obra = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_tipo_obra = db.Column(db.SmallInteger, nullable=False)
    foto = db.Column(db.Text, nullable = False)
    titulo = db.Column(db.String(64), nullable = False) #default = 'Sin Título',
    descripcion = db.Column(db.String(512), nullable=True)
    
    def __init__(self, id_usuario, id_tipo_obra, foto, titulo, descripcion = ""):  # , foto, titulo, id_usuario, id_tipo,
        self.id_usuario = id_usuario
        self.id_tipo_obra = id_tipo_obra
        self.foto = foto
        self.titulo = titulo
        self.descripcion = descripcion

    def a_diccionario(self):
        return {
            "id_obra" : self.id_obra,
            "id_usuario" : self.id_usuario,
            "id_tipo_obra" : self.id_tipo_obra,
            "foto" : self.foto,
            "titulo" : self.titulo,
            "descripcion" : self.descripcion
        }
