from flask import Flask, render_template, request

from routes.obraRoute import obra_bp
from routes.usuarioRoute import usuario_bp
from flask_cors import CORS
from database.db import db
from auth.login import lm

app = Flask(__name__)
#app.config.from_mapping
#app.debug = True
app.config['SECRET_KEY'] = 'top-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/arar_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

lm.init_app(app)
lm.login_view = "/"

CORS(app)

""" @app.route("/")
def inicio():
    return render_template('inicio.html') """#render_template("inicio.html")

app.register_blueprint(usuario_bp)
app.register_blueprint(obra_bp)


with app.app_context(): #lo puedo colocar aca o en el run es para crear las tablas
    db.create_all()