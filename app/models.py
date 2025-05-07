from app import db
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    correo = db.Column(db.String(150), unique=True, nullable=False)  
    contraseña = db.Column(db.String(150), nullable=False)

    def get_id(self):
        return str(self.id_usuario)
    
class Pelicula(db.Model):
    __tablename__ = 'pelicula'
    id_pelicula = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    director = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    fecha_lanzamiento = db.Column(db.Date, nullable=True)
    portada = db.Column(db.String(255), nullable=True)
    resenas = db.relationship('Resena', backref='pelicula', lazy=True)  # Relación con Resena

class Resena(db.Model):
    __tablename__ = 'resena'
    id_resena = db.Column(db.Integer, primary_key=True)
    comentario = db.Column(db.Text, nullable=False)
    puntuacion = db.Column(db.Integer, nullable=False)  # Correctamente definido
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    id_pelicula = db.Column(db.Integer, db.ForeignKey('pelicula.id_pelicula'), nullable=False)
    usuario = db.relationship('Usuario', backref='resenas')  # Relación con Usuario