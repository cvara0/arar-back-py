from database.db import db

class Obras(db.Model):
    id_obra = db.Column(db.Integer, primary_key = True)
    #id_usuario = db.Column(db.Integer, db.ForeingKey('usuarios.id_usuario'), nullable = False)
    id_tipo_obra = db.Column(db.SmallInteger, nullable = False)
    descripcion = db.Column(db.Text, nullable = True)
    #foto = db.Column(db.Text, nullable = False)
    #titulo = db.Column(db.String(100), nullable = False) #default = 'Sin Título',
    
    def __init__(self, id_tipo, descripcion): # , foto, titulo, id_usuario, id_tipo,
        #self.id_usuario = id_usuario
        self.id_tipo = id_tipo
        self.descripcion = descripcion
        #self.foto = foto
        #self.titulo = titulo
    
    def a_diccionario(self):
        return {
            'id_obra' : self.id_obra,
            'descripcion' : self.descripcion,
            'id_tipo' : self.id_tipo
        }