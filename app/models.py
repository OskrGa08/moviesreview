from app import db
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    correo = db.Column(db.String(150), unique=True)
    contraseña = db.Column(db.String(255))
    fecha_registro = db.Column(db.DateTime)

class Pelicula(db.Model):
    id_pelicula = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200))
    director = db.Column(db.String(150))
    descripcion = db.Column(db.Text)
    fecha_lanzamiento = db.Column(db.Date)
    portada = db.Column(db.String(255))  # Ruta del archivo de la portada
    resenas = db.relationship('Resena', backref='pelicula', lazy=True)  # Relación con las reseñas

class Resena(db.Model):
    id_resena = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))
    id_pelicula = db.Column(db.Integer, db.ForeignKey('pelicula.id_pelicula'))
    comentario = db.Column(db.Text)
    puntuacion = db.Column(db.Integer)
    fecha_resena = db.Column(db.DateTime)