from flask import Blueprint, abort, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from .models import Usuario, Pelicula, Resena, db
from datetime import datetime
import os
from flask import current_app
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Usuario, db

main = Blueprint('main', __name__)

@main.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contraseña = request.form['contraseña']

        # Verificar si el correo ya está registrado
        usuario_existente = Usuario.query.filter_by(correo=correo).first()
        if usuario_existente:
            flash('El correo ya está registrado.')
            return redirect(url_for('main.registro'))

        # Crear un nuevo usuario
        nuevo_usuario = Usuario(
            nombre=nombre,
            correo=correo,
            contraseña=generate_password_hash(contraseña, method='sha256')
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Usuario registrado exitosamente. Ahora puedes iniciar sesión.')
        return redirect(url_for('main.login'))

    return render_template('registro.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']

        # Verificar las credenciales
        usuario = Usuario.query.filter_by(correo=correo).first()
        if usuario and check_password_hash(usuario.contraseña, contraseña):
            login_user(usuario)
            return redirect(url_for('main.index'))
        else:
            flash('Correo o contraseña incorrectos.')

    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.')
    return redirect(url_for('main.index'))

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

        # Obtener la URL de la portada
        portada = request.form.get('portada', None)
        if not portada:
            portada = 'https://via.placeholder.com/150'  # URL predeterminada si no se proporciona ninguna

        nueva_pelicula = Pelicula(
            titulo=titulo,
            director=director,
            descripcion=descripcion,
            fecha_lanzamiento=fecha_lanzamiento,
            portada=portada
        )
        db.session.add(nueva_pelicula)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('nueva_pelicula.html')

@main.route('/pelicula/<int:id>', methods=['GET', 'POST'])
def pelicula(id):
    pelicula = Pelicula.query.get_or_404(id)  # Obtener la película por ID
    if request.method == 'POST':
        id_usuario = int(request.form['id_usuario'])  # ID del usuario que hace la reseña
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
        return redirect(url_for('main.pelicula', id=id))  # Recargar la página de detalles
    return render_template('pelicula.html', pelicula=pelicula)

@main.route('/resena/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_resena(id):
    resena = Resena.query.get_or_404(id)
    if resena.id_usuario != current_user.id_usuario:
        flash('No tienes permiso para editar esta reseña.')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        resena.comentario = request.form['comentario']
        resena.puntuacion = int(request.form['puntuacion'])
        db.session.commit()
        flash('Reseña actualizada exitosamente.')
        return redirect(url_for('main.pelicula', id=resena.id_pelicula))

    return render_template('editar_resena.html', resena=resena)

@main.route('/resena/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_resena(id):
    resena = Resena.query.get_or_404(id)
    if resena.id_usuario != current_user.id_usuario:
        flash('No tienes permiso para eliminar esta reseña.')
        return redirect(url_for('main.index'))

    db.session.delete(resena)
    db.session.commit()
    flash('Reseña eliminada exitosamente.')
    return redirect(url_for('main.pelicula', id=resena.id_pelicula))