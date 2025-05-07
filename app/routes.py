from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Usuario, Pelicula, Resena, db
from sqlalchemy.orm import joinedload
from datetime import datetime

main = Blueprint('main', __name__)

# Ruta para la página principal: muestra todas las películas y sus reseñas
@main.route('/')
def index():
    peliculas = Pelicula.query.options(
        joinedload(Pelicula.resenas).joinedload(Resena.usuario)
    ).all()
    return render_template('index.html', peliculas=peliculas)

# Ruta para ver los detalles de una película y agregar reseñas
@main.route('/pelicula/<int:id>', methods=['GET', 'POST'])
def detalle_pelicula(id):
    pelicula = Pelicula.query.get_or_404(id)
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('Debes iniciar sesión para agregar una reseña.')
            return redirect(url_for('main.login'))

        contenido = request.form['comentario']  # Cambiar 'comentario' a 'contenido'
        puntuacion = int(request.form['puntuacion'])
        nueva_resena = Resena(
            contenido=contenido,  # Usar 'contenido' en lugar de 'comentario'
            id_usuario=current_user.id_usuario,
            id_pelicula=pelicula.id_pelicula
        )
        db.session.add(nueva_resena)
        db.session.commit()
        flash('Reseña agregada exitosamente.')
        return redirect(url_for('main.detalle_pelicula', id=id))

    return render_template('detalle_pelicula.html', pelicula=pelicula)

# Ruta para editar una reseña
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
        return redirect(url_for('main.index'))

    return render_template('editar_resena.html', resena=resena)

# Ruta para eliminar una reseña
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
    return redirect(url_for('main.index'))

# Ruta para registrarse
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
            contraseña=generate_password_hash(contraseña, method='pbkdf2:sha256')
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Usuario registrado exitosamente. Ahora puedes iniciar sesión.')
        return redirect(url_for('main.login'))

    return render_template('registro.html')

# Ruta para iniciar sesión
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']

        # Verificar las credenciales
        usuario = Usuario.query.filter_by(correo=correo).first()
        if usuario and check_password_hash(usuario.contraseña, contraseña):
            login_user(usuario)
            flash('Has iniciado sesión exitosamente.', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Correo o contraseña incorrectos.', 'error')

    return render_template('login.html')

# Ruta para cerrar sesión
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.')
    return redirect(url_for('main.index'))

#Ruta para crear una nueva película
@main.route('/pelicula/nueva', methods=['GET', 'POST'])
@login_required
def nueva_pelicula():
    if request.method == 'POST':
        titulo = request.form['titulo']
        director = request.form['director']
        descripcion = request.form['descripcion']
        fecha_lanzamiento = request.form['fecha_lanzamiento']
        portada = request.form['portada']

        # Convertir la fecha de lanzamiento a un objeto datetime.date
        try:
            fecha_lanzamiento = datetime.strptime(fecha_lanzamiento, '%Y-%m-%d').date()
        except ValueError:
            flash('Formato de fecha inválido. Usa el formato AAAA-MM-DD.')
            return redirect(url_for('main.nueva_pelicula'))

        nueva_pelicula = Pelicula(
            titulo=titulo,
            director=director,
            descripcion=descripcion,
            fecha_lanzamiento=fecha_lanzamiento,
            portada=portada
        )
        db.session.add(nueva_pelicula)
        db.session.commit()
        flash('Película creada exitosamente.')
        return redirect(url_for('main.index'))

    return render_template('nueva_pelicula.html')