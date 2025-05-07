from app import db
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def get_id(self):
        return str(self.id_usuario)
    
class Pelicula(db.Model):
    id_pelicula = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200))
    director = db.Column(db.String(150))
    descripcion = db.Column(db.Text)
    fecha_lanzamiento = db.Column(db.Date)  # Asegúrate de que sea de tipo Date
    portada = db.Column(db.String(255))  # Ruta del archivo de la portada
    resenas = db.relationship('Resena', backref='pelicula', lazy=True)

class Resena(db.Model):
    id_resena = db.Column(db.Integer, primary_key=True)
    comentario = db.Column(db.Text)
    puntuacion = db.Column(db.Integer)
    fecha_resena = db.Column(db.DateTime, default=db.func.current_timestamp())
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    id_pelicula = db.Column(db.Integer, db.ForeignKey('pelicula.id_pelicula'), nullable=False)