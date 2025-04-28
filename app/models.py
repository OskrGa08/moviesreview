from . import db

class Usuario(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    correo = db.Column(db.String(150), unique=True)
    contraseña = db.Column(db.String(255))
    fecha_registro = db.Column(db.DateTime)

class Item(db.Model):
    id_item = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))  # 'Libro' o 'Película'
    titulo = db.Column(db.String(200))
    autor_director = db.Column(db.String(150))
    descripcion = db.Column(db.Text)
    fecha_lanzamiento = db.Column(db.Date)

class Resena(db.Model):
    id_resena = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))
    id_item = db.Column(db.Integer, db.ForeignKey('item.id_item'))
    comentario = db.Column(db.Text)
    puntuacion = db.Column(db.Integer)
    fecha_resena = db.Column(db.DateTime)
