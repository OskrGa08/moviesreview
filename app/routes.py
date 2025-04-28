from flask import Blueprint, render_template, request, redirect, url_for
from .models import Usuario, Pelicula, Resena, db
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    peliculas = Pelicula.query.all()  # Obtener todas las películas de la base de datos
    return render_template('index.html', peliculas=peliculas)

@main.route('/usuario/nuevo', methods=['GET', 'POST'])
def nuevo_usuario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        nuevo_usuario = Usuario(nombre=nombre, correo=correo, contraseña=contraseña)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('nuevo_usuario.html')

@main.route('/pelicula/nueva', methods=['GET', 'POST'])
def nueva_pelicula():
    if request.method == 'POST':
        titulo = request.form['titulo']
        director = request.form['director']
        descripcion = request.form['descripcion']
        fecha_lanzamiento = datetime.strptime(request.form['fecha_lanzamiento'], '%Y-%m-%d').date()
        portada = request.form['portada']  # Obtener la URL de la portada

        nueva_pelicula = Pelicula(
            titulo=titulo,
            director=director,
            descripcion=descripcion,
            fecha_lanzamiento=fecha_lanzamiento,
            portada=portada  # Guardar la URL de la portada
        )
        db.session.add(nueva_pelicula)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('nueva_pelicula.html')

@main.route('/pelicula/<int:id>/resena', methods=['GET', 'POST'])
def nueva_resena(id):
    pelicula = Pelicula.query.get_or_404(id)
    if request.method == 'POST':
        id_usuario = int(request.form['id_usuario'])  # Cambiar por el usuario autenticado
        comentario = request.form['comentario']
        puntuacion = int(request.form['puntuacion'])
        nueva_resena = Resena(
            id_usuario=id_usuario,
            id_pelicula=pelicula.id_pelicula,
            comentario=comentario,
            puntuacion=puntuacion
        )
        db.session.add(nueva_resena)
        db.session.commit()
        return redirect(url_for('main.pelicula', id=id))
    return render_template('nueva_resena.html', pelicula=pelicula)