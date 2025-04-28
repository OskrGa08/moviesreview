from flask import Blueprint, render_template, request, redirect, url_for
from .models import Pelicula, Resena, db  # Importar solo lo necesario

main = Blueprint('main', __name__)

@main.route('/')
def index():
    peliculas = Pelicula.query.all()  # Verifica que la tabla 'pelicula' exista
    return render_template('index.html', peliculas=peliculas)

@main.route('/pelicula/<int:id>', methods=['GET', 'POST'])
def pelicula(id):
    pelicula = Pelicula.query.get_or_404(id)
    if request.method == 'POST':
        comentario = request.form['comentario']
        puntuacion = int(request.form['puntuacion'])
        nueva_resena = Resena(
            id_usuario=1,  # Cambiar por el ID del usuario autenticado
            id_pelicula=pelicula.id_pelicula,
            comentario=comentario,
            puntuacion=puntuacion
        )
        db.session.add(nueva_resena)
        db.session.commit()
        return redirect(url_for('main.pelicula', id=id))
    return render_template('pelicula.html', pelicula=pelicula)